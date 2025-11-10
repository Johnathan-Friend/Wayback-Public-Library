<template>
  <v-container fluid class="fill-height pa-4">
    <v-row
      class="h-100"
      align="center"
      justify="center"
    >
      <v-col cols="12" md="6" lg="5">
        <div class="text-center mb-4">
          <h1 class="pb-4">Reservations</h1>
        </div>
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
        <v-card
          v-if="hasItemSelected"
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
              @click="reserveItem"
              :disabled="!hasItemSelected"
            >
              Reserve
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
  </v-container>
</template>

<script setup>
import api from '../api/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const emptyItemDetailState = {
  Description: "",
  ISBN: "",
  Quantity: "",
  Rating: "",
  Title: ""
}

const items = ref([])
const selectedItemID = ref(null)
const hasItemSelected = ref(false)
const itemDetails = ref(emptyItemDetailState)

onMounted(() => {
  loadItems()
})

async function loadItems() {
  try {
    items.value = await api.getAllItems()
  } catch (err) {
    console.error("Failed to load items:", err)
  }
}

async function fetchItemDetails() {
  if (!selectedItemID.value) {
    clearItemState()
    return
  }
  try {
    const selectedItem = items.value.find(item => item.ItemID === selectedItemID.value)
    itemDetails.value = await api.getItemDetails(selectedItem.ISBN)
    hasItemSelected.value = true
  } catch (error) {
    console.error("Failed to load item details:", error)
    clearItemState()
  }
}

function clearItemState() {
  itemDetails.value = emptyItemDetailState
  hasItemSelected.value = false
}

function reserveItem() {
  // Placeholder function - doesn't do anything yet
  console.log("Reserve button clicked for item:", selectedItemID.value)
}

function goBack() {
  router.push('/')
}
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}
</style>

