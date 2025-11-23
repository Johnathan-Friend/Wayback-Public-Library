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
            <v-autocomplete
              label="Search Members"
              :items="patrons"
              :item-title="formatPatronTitle"
              item-value="PatronID"
              v-model="selectedPatronID"
              variant="outlined"
              density="comfortable"
              class="pt-6"
            />
            <v-autocomplete
              label="Search Item ID"
              :items="items"
              item-title="ItemID"
              item-value="ItemID"
              v-model="selectedItemID"
              variant="outlined"
              density="comfortable"
            />
          <v-card-actions>
            <v-btn
              color="primary"
              variant="elevated"
              @click="addReservationEntry"
              :disabled="!selectedPatronID || !selectedItemID"
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
import { ref, computed, onMounted } from "vue"
import { mdiDelete } from "@mdi/js"
import { useRouter } from "vue-router"
import api from '../api/api'

const router = useRouter();
const items = ref([]);
const patrons = ref([]);
const selectedItemID = ref(null);
const selectedPatronID = ref(null);
const selectedFilter = ref('reservation');
const searchQuery = ref('');
const selectedSearchValue = ref(null);
const leftPanelError = ref(null);
const allReservations = ref([]);
const tableError = ref(null);

const reservationHeaders = [
  { title: "Reservation ID", key: "id" },
  { title: "Name/Item", key: "label" },
  { title: "Details", key: "details" },
  { title: "Actions", key: "actions", sortable: false }
];

const reservations = computed(() => {
  if (!searchQuery.value || !searchQuery.value.trim()) {
    return allReservations.value.map(formatReservation);
  }

  const query = searchQuery.value.trim();
  return allReservations.value
    .filter(reservation => {
      if (selectedFilter.value === 'reservation') {
        return reservation.ReservationID.toString().includes(query);
      } else if (selectedFilter.value === 'patron') {
        return reservation.PatronID.toString().includes(query);
      } else if (selectedFilter.value === 'item') {
        return reservation.ItemID.toString().includes(query);
      }
      return true;
    })
    .map(formatReservation);
});

const formatPatronTitle = (patron) => {
  return `${patron.FirstName} ${patron.LastName} (${patron.PatronID})`
}

function formatReservation(reservation) {
  return {
    id: reservation.ReservationID,
    label: `Patron ${reservation.PatronID} / Item ${reservation.ItemID}`,
    details: `Reserved: ${reservation.ReservationDate || 'N/A'} | Expires: ${reservation.ReservationExpirationDate || 'N/A'}`,
    reservationId: reservation.ReservationID
  };
}

async function loadReservations() {
  try {
    tableError.value = null;
    const reservations = await api.getAllReservations();
    const nonPickedUpReservations = reservations.filter(reservation => reservation.PickupDate === null || reservation.PickupDate === undefined || reservation.PickupDate === '');
    const today = new Date().toISOString().split('T')[0];
    for (const reservation of nonPickedUpReservations) {
      if (reservation.ReservationExpirationDate < today) {
        await performDeletion(reservation.ReservationID, false);
      }
    }
    allReservations.value = reservations.filter(reservation =>
      !reservation.PickupDate &&
      reservation.ReservationExpirationDate >= today
    );
  } catch (error) {
    console.error("Failed to load reservations:", error);
    tableError.value = error.response?.data?.detail || 'Failed to load reservations';
  }
}

async function loadItems() {
  try {
    const itemResults = await api.getAvailableItemsForCheckout();
    const reservedItemIDs = new Set(
      allReservations.value.map(reservation => reservation.ItemID)
    );
    items.value = itemResults.filter(item => !reservedItemIDs.has(item.ItemID));
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

async function addReservationEntry() {
  if (!selectedPatronID.value || !selectedItemID.value) {
    leftPanelError.value = "Please select both a patron and an item.";
    return;
  }

  leftPanelError.value = null;
  const reservationDate = calculateReservationDate();
  const expirationDate = calculateExpirationDate(reservationDate);
  
  try {
    await api.createReservation(selectedItemID.value, selectedPatronID.value, reservationDate, expirationDate);
  } catch (error) {
    console.error("Failed to create reservation:", error);
    leftPanelError.value = error.response?.data?.detail || 'Failed to create reservation';
    return;
  }
  
  await loadReservations();
  await loadItems();
  selectedPatronID.value = null;
  selectedItemID.value = null;
}

function calculateReservationDate() {
  return new Date().toISOString().split('T')[0];
}

function calculateExpirationDate(reservationStartDate) {
  const date = new Date(reservationStartDate);
  date.setDate(date.getDate() + 5);
  return date.toISOString().split('T')[0];
}

async function deleteReservation(item) {
  if (!confirm(`Are you sure you want to delete reservation ${item.id}?`)) {
    return;
  }
  await performDeletion(item.reservationId);
}

async function performDeletion(reservationID, shouldLoadReservations = true) {
  try {
    tableError.value = null;
    await api.deleteReservation(reservationID);
    if (shouldLoadReservations) {
      await loadReservations();
      await loadItems();
    }
  } catch (error) {
    console.error("Failed to delete reservation:", error);
    tableError.value = error.response?.data?.detail || 'Failed to delete reservation';
  }
}

function goBack() {
  router.push("/")
}

onMounted(async () => {
  await loadReservations();
  loadItems();
  loadPatrons();
});
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
