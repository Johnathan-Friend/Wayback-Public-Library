<template>
  <div class="checkin page">
    <div class="checkin-card">
      <h1>Check In</h1>
      <v-row class="h-100">
        <v-col cols="12" md="5" class="left-panel">
            <v-row class="search" justify="center">
                <v-autocomplete
                  label="Search Item"
                  :items="items"
                  item-title="ItemID" 
                  item-value="ItemID"
                  v-model="selectedItemID"
                  variant="outlined"
                  density="comfortable"
                  @update:modelValue="fetchItemDetails()"
                />
            </v-row>
        </v-col>
      </v-row>
      <v-alert
        v-if="successMessage"
        type="success"
        :text="successMessage"
        variant="elevated"
        class="mt-4"
      ></v-alert>
      <v-alert
        v-if="errorMessage"
        type="warning"
        :text="errorMessage"
        variant="elevated"
        class="mt-4 mb-8"
      ></v-alert>
      <div class="grid">
        <div class="labels">
          <label>Title</label>
          <input :value="title" disabled />
        </div>
        <div class="labels">
          <label>Member</label>
          <input :value="member" disabled />
        </div>
        <div class="labels">
          <label>Due Date</label>
          <input :value="dueDateDisplay" disabled />
        </div>
        <div class="labels">
          <label>Return Date</label>
          <input :value="returnDateDisplay" disabled />
        </div>
        <div class="labels">
          <label>Days Late (Calculated after check in)</label>
          <input :value="daysLateDisplay" disabled />
        </div>
        <div class="labels">
          <label>Fines (Calculated after check in)</label>
          <input :value="finesDisplay" disabled />
        </div>
      </div>
      <div class="d-flex justify-space-between align-center">
        <v-btn 
          color="primary" 
          @click="confirmCheckIn" 
          class="mr-2" 
          :disabled="!selectedItemID || !member"
        >
          Check In
        </v-btn>
        <div>
          <v-btn 
            color="secondary" 
            @click="resetFields" 
            class="mr-2"
          >
            Another Item
          </v-btn>
          <v-btn 
            color="black" 
            @click="goToHome" 
            variant="outlined"
          >
            Finish
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const items = ref([]);
const selectedItemID = ref(null);
const itemDetails = ref(null);

const title = ref(null);
const member = ref(null);
const dueDate = ref(null);
const returnDate = ref(null);
const daysLate = ref(0);
const fines = ref(0);

const dueDateDisplay = ref('');
const returnDateDisplay = ref('');
const daysLateDisplay = ref('---');
const finesDisplay = ref('---');
const successMessage = ref('');
const errorMessage = ref('');

async function loadItems() {
  try {
    items.value = await api.getAllItems();
  } catch (err) {
    console.error("Failed to load items:", err);
  }
}

async function fetchItemDetails() {
  errorMessage.value = '';
  if (!selectedItemID.value) {
    resetFields();
    return
  }
  try {
    const selectedItem = items.value.find(item => item.ItemID === selectedItemID.value);
    itemDetails.value = await api.getItemDetails(selectedItem.ISBN);
    title.value = itemDetails.value.Title;
    const transaction = await api.getTransactionByItemId(selectedItemID.value);

    if (transaction.DateReturned) {
      resetFields();
      throw new Error('Item not checked out');
    }

    if (transaction) {
      if (transaction.PatronID) {
        member.value = transaction.PatronID;
      } else {
        member.value = null;
      }
      if (transaction.DateDue) {
        const parsedDue = new Date(transaction.DateDue);
        if (!isNaN(parsedDue.getTime())) {
          dueDate.value = parsedDue;
          dueDateDisplay.value = parsedDue.toLocaleDateString();
        } else {
          dueDate.value = null;
          dueDateDisplay.value = '';
        }
      } else {
        dueDate.value = null;
        dueDateDisplay.value = '';
      }
    } else {
      member.value = null;
      dueDate.value = null;
      dueDateDisplay.value = '';
    }
    
    const today = new Date();
    returnDate.value = today;
    returnDateDisplay.value = today.toLocaleDateString();

  } catch (err) {
    console.error("Failed to load items:", err);
    resetFields();
    errorMessage.value = 'That item is not checked out. Scan another item to check it in please.';
  }
}

function resetFields() {
  selectedItemID.value = null;
  itemDetails.value = null;
  title.value = null;
  member.value = null;
  dueDate.value = null;
  returnDate.value = null;
  daysLate.value = 0;
  fines.value = 0;
  dueDateDisplay.value = '';
  returnDateDisplay.value = '';
  daysLateDisplay.value = '---';
  finesDisplay.value = '---';
  successMessage.value = '';
  errorMessage.value = '';
}

async function confirmCheckIn() {
  if (!selectedItemID.value || !member.value || !returnDate.value) {
    errorMessage.value = 'Missing required information for check-in';
    return;
  }

  try {
    const returnDateFormatted = returnDate.value.toISOString().split('T')[0];
    const response = await api.checkInItem(member.value, selectedItemID.value, returnDateFormatted);
    successMessage.value = `Successfully returned: ${title.value} for ${response.PatronName}`;
    daysLateDisplay.value = response.DaysLate;
    finesDisplay.value = response.FeeCharged;
    errorMessage.value = '';
    selectedItemID.value = null;
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || 'Failed to check in item';
    successMessage.value = '';
  }
}

function goToHome() {
  router.push('/');
}

onMounted(() => {
  loadItems();
});

</script>

<style scoped>

  .checkin-page {
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(to bottom right, #3b82f6, #7cd0c3);
    padding: 16px;
  }

  .checkin-card {
    width: 85%;
    max-width: 900px;
    margin: 100px auto;
    background: #fff;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.06);
  }

  h1 {
    text-align: center;
    margin: 0 0 12px 0;
  }

  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr; 
    gap: 12px;
    margin-top: 12px;
  }

  .labels label {
    font-weight: 600;
    margin-bottom: 4px;
    display: block;
  }

  .actions {
    display: flex;
    justify-content: center;
    gap: 10px;
  }
</style>
