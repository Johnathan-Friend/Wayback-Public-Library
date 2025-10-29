<template>
  <v-container fluid class="fill-height pa-4">
    <v-row class="h-100 membership-center" v-if="!isPatronSelected">
      <v-col cols="12" md="8">
        <h1 class="pb-5">Member Lookup</h1>
        <v-autocomplete
          label="Search Members"
          :items="patrons"
          :item-title="formatPatronTitle"
          item-value="PatronID"
          v-model="selectedPatronID"
          variant="outlined"
          density="comfortable"
        />
        <v-btn color="primary" @click="selectPatron()" v-bind:disabled="!selectedPatronID">Get Member Details</v-btn>
      </v-col>
    </v-row>
    <v-row class="h-100" v-else>
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
      <v-col cols="12" md="7" class="right-panel">
        <div class="table-placeholder">
          <p>table will go here</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'

const isPatronSelected = ref(false);
const items = ref([]);
const patrons = ref([]);
const selectedItemID = ref(null);
const selectedPatronID = ref(null);
const itemDetails = ref(null);

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
  if (!selectedItemID.value) return
  
  try {
    itemDetails.value = await api.getItemDetails(selectedItemID.value);
  } catch (err) {
    console.error("Failed to load items:", err);
  }
}

onMounted(() => {
  loadItems();
  loadPatrons();
});

const formatPatronTitle = (patron) => {
  return `${patron.FirstName} ${patron.LastName} (${patron.PatronID})`
}

function selectPatron() {
  isPatronSelected.value = true;
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
