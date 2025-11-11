<template>
  <v-container fluid class="fill-height pa-4">
    <v-row
      class="h-100"
      align="center"
      justify="center"
    >
      <v-col cols="12" md="6" lg="5">
        <div class="text-center mb-4">
          <h1 class="pb-4">Patron Membership</h1>
          <v-btn
            color="primary"
            variant="elevated"
            @click="showNewPatronDialog = true"
            class="mb-4"
          >
            New Patron
          </v-btn>
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
          v-if="hasPatronSelected"
          class="pa-4 mt-4"
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
                <div>{{ patronDetails.MembershipExpiration || 'Not set' }}</div>
              </div>
              <div class="pb-2">
                <strong>Fee Balance:</strong>
                <div>${{ patronDetails.FeeBalance || '0.00' }}</div>
              </div>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              variant="elevated"
              @click="renewMembership"
              :disabled="!hasPatronSelected"
            >
              Renew Membership
            </v-btn>
            <v-btn
              color="secondary"
              variant="elevated"
              @click="payPatronFee"
              :disabled="!hasPatronSelected"
            >
              Pay Fee
            </v-btn>
            <v-btn
              color="red"
              variant="elevated"
              @click="showDeleteDialog = true"
              :disabled="!hasPatronSelected"
            >
              Delete Patron
            </v-btn>
          </v-card-actions>
        </v-card>
        <div class="d-flex justify-end mt-4">
          <v-btn color="black" @click="goBack" variant="outlined">
            Back to Home
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- New Patron Dialog -->
    <v-dialog v-model="showNewPatronDialog" max-width="500" persistent>
      <v-card class="pa-6">
        <v-card-title class="text-h6">
          <b>New Patron</b>
        </v-card-title>
        <v-card-text>
          <v-text-field
            label="First Name"
            v-model="newPatronFirstName"
            variant="outlined"
            class="mb-4"
          />
          <v-text-field
            label="Last Name"
            v-model="newPatronLastName"
            variant="outlined"
          />
          <v-alert
            v-if="newPatronError"
            type="error"
            :text="newPatronError"
            variant="elevated"
            class="mt-4"
          />
        </v-card-text>
        <v-card-actions class="d-flex justify-space-between">
          <v-btn color="green" variant="elevated" @click="createNewPatron">
            Create
          </v-btn>
          <v-btn color="red" variant="text" @click="cancelNewPatron">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="600" persistent>
      <v-card class="pa-6">
        <v-card-title class="text-h6">
          <b>Delete Patron</b>
        </v-card-title>
        <v-card-text>
          Are you sure you want to delete patron {{ patronDetails.FirstName }} {{ patronDetails.LastName }} (ID: {{ patronDetails.PatronID }})?
        </v-card-text>
        <v-card-actions class="d-flex justify-space-between">
          <v-btn color="red" variant="elevated" @click="confirmDelete">
            Delete
          </v-btn>
          <v-btn color="black" variant="text" @click="showDeleteDialog = false">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const emptyPatronState = {
  FirstName: "",
  LastName: "",
  PatronID: "",
  MembershipExpiration: "",
  FeeBalance: ""
}

const patrons = ref([])
const selectedPatronID = ref(null)
const hasPatronSelected = ref(false)
const patronDetails = ref(emptyPatronState)
const showNewPatronDialog = ref(false)
const showDeleteDialog = ref(false)
const newPatronFirstName = ref('')
const newPatronLastName = ref('')
const newPatronError = ref(null)

onMounted(() => {
  loadPatrons()
})

async function loadPatrons() {
  try {
    patrons.value = await api.getAllPatrons()
  } catch (err) {
    console.error("Failed to load patrons:", err)
  }
}

async function fetchPatronDetails() {
  if (!selectedPatronID.value) {
    clearPatronState()
    return
  }
  try {
    patronDetails.value = await api.getPatronDetails(selectedPatronID.value)
    hasPatronSelected.value = true
  } catch (error) {
    console.error("Failed to load patron details:", error)
    clearPatronState()
  }
}

function clearPatronState() {
  patronDetails.value = emptyPatronState
  hasPatronSelected.value = false
}

const formatPatronTitle = (patron) => {
  return `${patron.FirstName} ${patron.LastName} (${patron.PatronID})`
}

function goBack() {
  router.push('/')
}

async function createNewPatron() {
  newPatronError.value = null
  if (!newPatronFirstName.value || !newPatronLastName.value) {
    newPatronError.value = 'First name and last name are required'
    return
  }
  try {
    const newPatron = await api.createPatron(newPatronFirstName.value, newPatronLastName.value)
    await loadPatrons()
    selectedPatronID.value = newPatron.PatronID
    await fetchPatronDetails()
    cancelNewPatron()
  } catch (error) {
    console.error("Failed to create patron:", error)
    newPatronError.value = error.response?.data?.detail || 'Failed to create patron'
  }
}

function cancelNewPatron() {
  showNewPatronDialog.value = false
  newPatronFirstName.value = ''
  newPatronLastName.value = ''
  newPatronError.value = null
}

async function renewMembership() {
  if (!hasPatronSelected.value) return
  
  let base_date = new Date()
  if (patronDetails.value.MembershipExpiration) {
    const old_date = new Date(patronDetails.value.MembershipExpiration)
    if (!isNaN(old_date.getTime()) && old_date > base_date) {
      base_date = old_date
    }
  }

  // New expiration = +2 year from base if base date is greater than today
  const new_exp = new Date(base_date)
  new_exp.setFullYear(base_date.getFullYear() + 2)
  const expirationDate = new_exp.toISOString().split('T')[0]
  // this could be ommited completely.
  const ok = window.confirm(`Renew membership until ${expirationDate}?`)
  if (!ok) return

  try {
    await api.updatePatron(selectedPatronID.value, {
      MembershipExpiration: expirationDate
    })
    await fetchPatronDetails()
  } catch (error) {
    console.error("Failed to renew membership:", error)
    alert('Failed to renew membership: ' + (error.response?.data?.detail || 'Unknown error'))
  }
}

async function confirmDelete() {
  if (!hasPatronSelected.value) return
  
  try {
    await api.deletePatron(selectedPatronID.value)
    showDeleteDialog.value = false
    clearPatronState()
    selectedPatronID.value = null
    await loadPatrons()
  } catch (error) {
    console.error("Failed to delete patron:", error)
    alert('Failed to delete patron: ' + (error.response?.data?.detail || 'Unknown error'))
  }
}

async function payPatronFee() {
  if (!hasPatronSelected.value) return

  try {
    patronDetails.value = await api.updatePatronFee(patronDetails.value.PatronID, "0");
  } catch(error) {
    console.error(error);
    alert('Failed to delete patron: ' + (error.response?.data?.detail || 'Unknown error'))
  }
}
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}
</style>

