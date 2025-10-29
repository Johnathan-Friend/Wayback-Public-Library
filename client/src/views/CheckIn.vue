<script setup lang="ts">

</script>

<template>
  <h1>Check In</h1>
  <h2>Test</h2>

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
          />
          <v-btn color="primary" @click="fetchItemDetails()" v-bind:disabled="!selectedItemID">Search Item</v-btn>
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

</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'

const items = ref([]);
const selectedItemID = ref(null);
const itemDetails = ref(null);

const Title = ref(null);
const Member = ref(null);
const DueDate = ref(null);
const ReturnDate = ref(null);
const DaysLate = ref(null);
const Fines = ref(null);

async function loadItems() {
  try {
    items.value = await api.getAllItems();
  } catch (err) {
    console.error("Failed to load items:", err);
  }
}

async function fetchItemDetails() {
  if (!selectedItemID.value) return
  
  try {
    itemDetails.value = await api.getItemDetails(selectedItemID.value);
  } catch (err) {
    console.error("Failed to load items:", err);
  }
}

onMounted(() => {
  loadItems();
});

</script>

<style scoped>

</style>