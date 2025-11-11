<script setup lang="ts">
import api from '../api/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { mdiBookOpenPageVariant } from '@mdi/js'

const router = useRouter();
const selectedBranch = ref(null);
const branchData = ref([]);

onMounted(() => {
  loadBranches();
});

function goToCheckIn() {
  router.push({name: 'CheckIn', params: { branchID: selectedBranch.value } });
}

function goToCheckOut() {
  router.push({name: 'CheckOut', params: { branchID: selectedBranch.value } });
}

async function loadBranches() {
  try {
    branchData.value = await api.getBranches();
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <v-container
    fluid
    class="d-flex justify-center align-center main-container"
  >
    <v-card
      class="pa-10 text-center elevation-3"
      width="400"
      rounded="xl"
    >
      <v-icon :icon="mdiBookOpenPageVariant" size="72" color="primary" class="mb-6"/>
      <h1 class="mb-8 library-title">Wayback Public Library</h1>
      <v-select
        label="Select Branch"
        :items="branchData"
        item-title="Address"
        item-value="BranchID"
        variant="outlined"
        v-model="selectedBranch"
      ></v-select>
      <div class="d-flex justify-center gap-4">
        <v-btn
          color="secondary"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToCheckOut"
          :disabled="!selectedBranch"
        >
          Check Out
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToCheckIn"
          :disabled="!selectedBranch"
        >
          Check In
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
.main-container {
  min-height: 100vh;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.library-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.gap-4 {
  gap: 1rem;
}
</style>
