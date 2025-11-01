<template>
  <h1>Check In</h1>

<v-row class="h-100">
  <v-col cols="12" md="5" class="left-panel">
      <v-row class="search">
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


    <div>
      <label>Title</label>
      <input :value="title" disabled />
    </div>

    <div>
      <label>Member</label>
      <input :value="member" disabled />
    </div>

    <div>
      <label>Due Date</label>
      <input :value="dueDateDisplay" disabled />
    </div>

    <div>
      <label>Return Date</label>
      <input :value="returnDateDisplay" disabled />
    </div>

    <div>
      <label>Days Late</label>
      <input :value="daysLateDisplay" disabled />
    </div>

    <div>
      <label>Fines</label>
      <input :value="finesDisplay" disabled />
    </div>

    <div>
      <v-btn color="primary" @click="confirmCheckIn" class="mr-2" :disabled="!selectedItemID || !patronID">Confirm</v-btn>
      <v-btn color="secondary" @click="resetFields" class="mr-2">Another Item</v-btn>
      <v-btn color="black" @click="goToHome" variant="outlined">Finish</v-btn>
    </div>

    <v-alert
      v-if="successMessage"
      type="success"
      :text="successMessage"
      variant="elevated"
      class="mt-4"
    ></v-alert>

    <v-alert
      v-if="errorMessage"
      type="error"
      :text="errorMessage"
      variant="elevated"
      class="mt-4"
    ></v-alert>

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
const patronID = ref(null);
const dueDate = ref(null);
const returnDate = ref(null);
const daysLate = ref(0);
const fines = ref(0);

const dueDateDisplay = ref('');
const returnDateDisplay = ref('');
const daysLateDisplay = ref(0);
const finesDisplay = ref('$0.00');
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
  if (!selectedItemID.value) {
    itemDetails.value = null;
    title.value = null;
    returnDate.value = null;
    returnDateDisplay.value = '';
    daysLate.value = 0;
    daysLateDisplay.value = 0;
    fines.value = 0;
    finesDisplay.value = '$0.00';
    successMessage.value = '';
    errorMessage.value = '';
    return
  }
  try {
    const selectedItem = items.value.find(item => item.ItemID === selectedItemID.value);
    itemDetails.value = await api.getItemDetails(selectedItem.ISBN);
    title.value = itemDetails.value.Title;
    
    const today = new Date();
    returnDate.value = today;
    returnDateDisplay.value = today.toLocaleDateString();
    
    if (dueDate.value && returnDate.value) {
      const due = new Date(dueDate.value);
      const returned = new Date(returnDate.value);
      const diffTime = returned - due;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      daysLate.value = diffDays > 0 ? diffDays : 0;
    } else {
      daysLate.value = 0;
    }
    
    daysLateDisplay.value = daysLate.value;
    fines.value = daysLate.value * 1;
    finesDisplay.value = `$${fines.value.toFixed(2)}`;
    errorMessage.value = '';
  } catch (err) {
    console.error("Failed to load items:", err);
    errorMessage.value = 'Failed to load item details';
  }
}

function resetFields() {
  selectedItemID.value = null;
  itemDetails.value = null;
  title.value = null;
  member.value = null;
  patronID.value = null;
  dueDate.value = null;
  returnDate.value = null;
  daysLate.value = 0;
  fines.value = 0;
  dueDateDisplay.value = '';
  returnDateDisplay.value = '';
  daysLateDisplay.value = 0;
  finesDisplay.value = '$0.00';
  successMessage.value = '';
  errorMessage.value = '';
}

async function confirmCheckIn() {
  if (!selectedItemID.value || !patronID.value || !returnDate.value) {
    errorMessage.value = 'Missing required information for check-in';
    return;
  }

  try {
    const returnDateFormatted = returnDate.value.toISOString().split('T')[0];
    const response = await api.checkInItem(patronID.value, selectedItemID.value, returnDateFormatted);
    
    successMessage.value = `Successfully returned: ${title.value} for ${response.PatronName}`;
    errorMessage.value = '';
    
    setTimeout(() => {
      resetFields();
    }, 3000);
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

</style>