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
                <div>0</div>
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
              :disabled="patronCannotCheckOutItems || !hasPatronSelected"
            >
              Continue
            </v-btn>
          </v-card-actions>
        </v-card>
        <div class="d-flex justify-end mt-10">
          <v-btn color="red" @click="goBack">
            Cancel
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
        <div class=" mt-10">
          <v-btn color="green" variant="elevated" class="mr-4" @click="completeTransaction">
            Complete Transaction
          </v-btn>
          <v-btn color="red" variant="elevated" @click="togglePatron">
            Cancel
          </v-btn>
        </div>
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
    </v-row>

  </v-container>
</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter();

const emptyItemDetailState = {
  Description: "",
  ISBN: "",
  Quantity: "",
  Rating: "",
  Title: ""
};
const emptyPatronState = {};

const isPatronSelected = ref(false);
const items = ref([]);
const patrons = ref([]);
const selectedItemID = ref(null);
const selectedPatronID = ref(null);
const hasItemSelected = ref(false);
const hasPatronSelected = ref(false);
const itemDetails = ref(emptyItemDetailState);
const patronDetails = ref(emptyPatronState);
const patronCannotCheckOutItems = ref(false);
const checkedOutItems = ref([]);

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
    patronDetails.value = emptyPatronState;
    hasPatronSelected.value = false;
    return;
  }
  try {
    patronDetails.value = await api.getPatronDetails(selectedPatronID.value);
    hasPatronSelected.value = true;
  } catch (error) {
    console.error("Failed to load Patrons:", err);
  }
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
  if (checkedOutItems.value.length === 0) return;
  console.log("Completing transaction for items:", checkedOutItems.value);
  checkedOutItems.value = [];
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

- need to add query to create transaction when added to table and show transaction details
- need to go back to home (or index) after clicking complete transaction
- need to add limit of items to be added based on total number of books currently checked out by user
- need to implement logic of retrieving total number of items checked out by user
- need to add validation for if a user can checkout books on member lookup screen
- make it look prettier it is mad digusting lol
-->