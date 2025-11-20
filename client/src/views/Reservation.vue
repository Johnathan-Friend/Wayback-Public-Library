<template>
  <v-container fluid class="pa-4">
    <div class="text-center">
        <h1 class="pb-5">Reservation System</h1>
    </div>
    <v-row class="h-100" align="start" justify="center">
      <v-col cols="12" md="4" lg="5">
        <v-card class="pa-4" variant="outlined">
            <h3>Create Reservation:</h3>
            <v-alert
                v-if="leftPanelError"
                type="error"
                :text="leftPanelError"
                variant="elevated"
                title="Error"
            ></v-alert>   
          
            <!-- TODO: Need to add inputs to create a reservation -->

          <v-card-actions>
            <v-btn
              color="primary"
              variant="elevated"
              @click="addReservationEntry"
              :disabled="!selectedSearchValue"
            >
              Create Reservation
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="8" lg="7">
        <v-row class="mb-4" align="center">
            <v-col cols="12" md="8">
                <v-text-field
                label="Search"
                v-model="searchQuery"
                variant="outlined"
                density="comfortable"
                clearable
                @input="fetchDetails"
                />
            </v-col>
            <v-col cols="12" md="4">
                <v-select
                label="Filter By"
                :items="[
                    { title: 'Reservation Number', value: 'reservation' },
                    { title: 'Patron', value: 'patron' },
                    { title: 'Item', value: 'item' }
                ]"
                v-model="selectedFilter"
                variant="outlined"
                density="comfortable"
                @update:modelValue="fetchDetails"
                />
            </v-col>
        </v-row>
        <v-alert
          v-if="tableError"
          type="error"
          :text="tableError"
          variant="elevated"
          title="Error"
        ></v-alert>
        <v-data-table
          :headers="reservationHeaders"
          :items="reservations"
          item-value="id"
          hide-default-footer
          class="elevation-1"
          dense
        >
          <template #item.actions="{ item }">
            <v-btn
              :icon="mdiDelete"
              color="red"
              variant="text"
              @click="deleteReservation(item)"
            ></v-btn>
          </template>
          <template #no-data>
            <p class="text-center">No reservations yet.</p>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <div class="mt-10 d-flex justify-center">
        <v-btn color="black" variant="outlined" @click="goBack">
            Back to Home
        </v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { ref } from "vue"
import { mdiDelete } from "@mdi/js"
import { useRouter } from "vue-router"

const router = useRouter();
const selectedFilter = ref('reservation');
const searchQuery = ref('');
const selectedSearchValue = ref(null);
const leftPanelError = ref(null);
const reservations = ref([]);
const tableError = ref(null);

const reservationHeaders = [{ title: "Reservation ID", key: "id" },{ title: "Name/Item", key: "label" },{ title: "Details", key: "details" },{ title: "Actions", key: "actions", sortable: false }];

// Placeholder: will need to be replaced by real lookup API
async function fetchDetails() {
  // Example call — adjust to your API needs
  await api.search({
    filter: selectedFilter.value,
    query: searchQuery.value
  });
}

function addReservationEntry() {
  reservations.value.push({
    id: Date.now(),
    label: "Example Reservation Entry",
    details: "Details go here"
  })
}

function deleteReservation(item) {
  reservations.value = reservations.value.filter(r => r.id !== item.id)
}

function goBack() {
  router.push("/")
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
