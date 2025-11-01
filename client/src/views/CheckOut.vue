<template>
  <v-container fluid class="fill-height pa-4">
    
    <!-- Patron Selection -->
    <v-row
      class="h-100"
      align="center"
      justify="center"
      v-if="!isPatronSelected"
    >
      <v-col cols="12" md="6" lg="5">
        <div class="text-center">
          <h1 class="pb-5">Member Lookup</h1>
        </div>
        <v-autocomplete
          label="Search Members"
          :items="patrons"
          :item-title="formatPatronTitle"
          item-value="PatronID"
          v-model="selectedPatronID"
          variant="outlined"
          density="comfortable"
          @update:modelValue="fetchPatronDetails()"
        />
        <v-alert
          v-if="patronSelectionError"
          type="error"
          :text="patronSelectionError"
          variant="elevated"
          title="Warning"
          color="red-darken-2"
        >
        </v-alert>
        <v-card
          class="pa-4 mt-4 pb-5"
          variant="outlined"
        >
          <v-card-title class="font-weight-bold">
            {{ patronDetails.FirstName }} {{ patronDetails.LastName }}
          </v-card-title>
          <v-card-subtitle class="text-medium-emphasis">
            Patron ID: {{ patronDetails.PatronID }}
          </v-card-subtitle>
          <v-divider class="my-3"></v-divider>
          <v-card-text>
            <div class="d-flex flex-column gap-2">
              <div class="pb-2">
                <strong>Membership Expires:</strong>
                <div>{{ patronDetails.MembershipExpiration }}</div>
              </div>
              <div class="pb-2">
                <strong>Number of Items Checked Out:</strong>
                <div>{{ patronDetails.ItemsCheckedOut }}</div>
              </div>
              <div>
                <strong>Fee Balance:</strong>
                <div>${{ patronDetails.FeeBalance }}</div>
              </div>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn
              @click="togglePatron"
              color="primary"
              variant="elevated"
              :disabled="!patronCanCheckoutItems || !hasPatronSelected"
            >
              Continue
            </v-btn>
          </v-card-actions>
        </v-card>
        <div class="d-flex justify-end mt-10">
          <v-btn color="black" @click="goBack" variant="outlined">
            Cancel Checkout
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Item Selection and Transaction Creation -->
    <v-row
      class="h-100"
      align="center"
      justify="center"
      v-else
    >
      <v-col cols="12" md="6" lg="5">
        <div>
          <h1 class="pb-5">Item Lookup</h1>
        </div>
        <v-autocomplete
          label="Search Item ID"
          :items="items"
          item-title="ItemID"
          item-value="ItemID"
          v-model="selectedItemID"
          variant="outlined"
          density="comfortable"
          @update:modelValue="fetchItemDetails()"
        />
        <v-card
          class="pa-4 mt-4"
          variant="outlined"
        >
          <v-card-title class="font-weight-bold">
            {{ itemDetails.Title }}
          </v-card-title>
          <v-card-subtitle class="text-medium-emphasis">
            ISBN: {{ itemDetails.ISBN }}
          </v-card-subtitle>
          <v-divider class="my-3"></v-divider>
          <v-card-text>
            <div class="d-flex flex-column gap-2">
              <div class="pb-2">
                <strong>Description:</strong>
                <div>{{ itemDetails.Description }}</div>
              </div>
              <div class="pb-2">
                <strong>Quantity:</strong>
                <div>{{ itemDetails.Quantity }}</div>
              </div>
              <div>
                <strong>Rating:</strong>
                <div>{{ itemDetails.Rating }}</div>
              </div>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn 
              color="primary" 
              variant="elevated" 
              @click="checkOutItem"
              :disabled="!hasItemSelected">
                Check Out
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" lg="5">
      <v-data-table
          :items="checkedOutItems"
          hide-default-footer
          class="elevation-1"
          dense
        >
        <template #no-data>
          <p class="text-center">No items selected yet.</p>
        </template>
      </v-data-table>
    </v-col>
    <div class="mt-10 d-flex">
      <v-btn color="green" variant="elevated" class="mr-4" @click="completeTransaction">
        Complete Transaction
      </v-btn>
      <v-btn color="black" variant="outlined" @click="togglePatron">
        Go Back
      </v-btn>
    </div>
  </v-row>
  </v-container>
  <v-dialog v-model="showConfirmDialog" max-width="600" persistent>
    <v-card class="pa-6">
      <v-card-title class="text-h6">
        <b>Confirm Transaction</b>
      </v-card-title>
      <v-card-text>
        You are about to check out
        <strong>{{ checkedOutItems.length }}</strong>
        {{ checkedOutItems.length === 1 ? 'item' : 'items' }} for member {{ patronDetails.FirstName }} {{ patronDetails.LastName }} (ID: {{ patronDetails.PatronID }}).
        Are you sure you want to continue?
      </v-card-text>
      <v-card-actions class="d-flex justify-space-between">
        <v-btn color="green" variant="elevated" :prepend-icon="mdiCheck" @click="confirmTransaction">
          Confirm
        </v-btn>
        <v-btn color="red" variant="text" @click="cancelTransaction">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { mdiCheck } from '@mdi/js'

const router = useRouter();

const emptyItemDetailState = {
  Description: "",
  ISBN: "",
  Quantity: "",
  Rating: "",
  Title: ""
};
const emptyPatronState = {
  FirstName: "",
  LastName: "",
  PatronID: "",
  MembershipExpiration: "",
  FeeBalance: "",
  ItemsCheckedOut: ""
};
const maximumNumberOfItemsCheckoutAtOnce = 20;

const isPatronSelected = ref(false);
const items = ref([]);
const patrons = ref([]);
const selectedItemID = ref(null);
const selectedPatronID = ref(null);
const hasItemSelected = ref(false);
const hasPatronSelected = ref(false);
const itemDetails = ref(emptyItemDetailState);
const patronDetails = ref(emptyPatronState);
const patronCanCheckoutItems = ref(false);
const checkedOutItems = ref([]);
const numberOfItemsAvailableToCheckout = ref(0);
const patronSelectionError = ref(null);
const showConfirmDialog = ref(false);

onMounted(() => {
  loadItems();
  loadPatrons();
});

async function loadItems() {
  try {
    items.value = await api.getAllItems();
  } catch (err) {
    console.error("Failed to load items:", err);
  }
}

async function loadPatrons() {
  try {
    patrons.value = await api.getAllPatrons();
  } catch (err) {
    console.error("Failed to load patrons:", err);
  }
}

async function fetchItemDetails() {
  if (!selectedItemID.value) {
    itemDetails.value = emptyItemDetailState;
    hasItemSelected.value = false;
    return
  }
  try {
    const selectedItem = items.value.find(item => item.ItemID === selectedItemID.value);
    itemDetails.value = await api.getItemDetails(selectedItem.ISBN);
    hasItemSelected.value = true;
  } catch (err) {
    console.error("Failed to load items:", err);
  }
}

async function fetchPatronDetails() {
  if (!selectedPatronID.value) {
    clearPatronState()
    return;
  }
  try {
    clearPatronState();
    patronDetails.value = await api.getPatronDetails(selectedPatronID.value);
    patronDetails.value.ItemsCheckedOut = await api.getPatronNumberOfBooksCheckedOut(selectedPatronID.value);
    checkPatronCheckoutStatus();
    hasPatronSelected.value = true;
  } catch (error) {
    console.error("Failed to load Patrons:", err);
  }
}

function checkPatronCheckoutStatus() {
  const itemsCheckedOut = patronDetails.value.ItemsCheckedOut;
  const feeBalance = patronDetails.value.FeeBalance;
  const membershipExpiration = new Date(patronDetails.value.MembershipExpiration);
  const today = new Date();
  if (itemsCheckedOut === '' || itemsCheckedOut >= maximumNumberOfItemsCheckoutAtOnce) {
    patronSelectionError.value = 'Patron has the maximum number of items checked out. Cannot checkout at this time.';
    return;
  }
  if (feeBalance === '' || feeBalance > 0) {
    patronSelectionError.value = 'Patron has an outstanding fee balance. Cannot checkout at this time.';
    return;
  }
  if (membershipExpiration <= today) {
    patronSelectionError.value = 'Membership has exprired, please renew membership to checkout books. Cannot check out at this time.';
    return;
  }
  numberOfItemsAvailableToCheckout.value = maximumNumberOfItemsCheckoutAtOnce - itemsCheckedOut;
  patronCanCheckoutItems.value = true;
}

function clearPatronState() {
  patronSelectionError.value = null;
  patronCanCheckoutItems.value = false;
  patronDetails.value = emptyPatronState;
  hasPatronSelected.value = false;
}

const formatPatronTitle = (patron) => {
  return `${patron.FirstName} ${patron.LastName} (${patron.PatronID})`
}

function togglePatron() {
  selectedItemID.value = null;
  itemDetails.value = {};
  hasItemSelected.value = false;
  checkedOutItems.value = [];
  isPatronSelected.value = !isPatronSelected.value;
}

function goBack() {
  router.push('/');
}

function checkOutItem() {
  if (hasItemSelected.value) {
    checkedOutItems.value.push({ ...itemDetails.value });
    selectedItemID.value = null;
    hasItemSelected.value = false;
  }
}

function completeTransaction() {
  showConfirmDialog.value = true;
}

function confirmTransaction() {
  showConfirmDialog.value = false;
  router.push('/');
}

function cancelTransaction() {
  showConfirmDialog.value = false;
}
</script>

<style scoped>
.left-panel {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.right-panel {
  padding: 16px;
}

.table-placeholder {
  border: 2px dashed #ccc;
  border-radius: 8px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
}

.search {
  gap: 16px;
  padding: 16px;
}

.membership-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<!-- 
TODO:

- need to implement api to create transaction when added to table and show transaction details
- need to limit number of items to be added to transaction list based on total number of books currently checked out by user
- need to only show items that are available for checkout (items not destoryed or currently checked out)
- replace table data showing item details to show transaction once created
- add delete button on table to delete transaction or essentially (check in) the item
- (optionally) add some styling because it looks booty rn
-->