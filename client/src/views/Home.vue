<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function goToCheckIn() {
  router.push('/checkin');
}
function goToCheckOut() {
  router.push('/checkout');
}
</script>

<template>
  <v-container class="d-flex justify-center align-center fill-height">
    <div class="text-center">
      <h1 class="mb-6">Wayback Public Library</h1>

      <div class="d-flex justify-center gap-4">
        <v-btn color="primary" @click="goToCheckIn">
          Check In
        </v-btn>

        <v-btn color="secondary" @click="goToCheckOut">
          Check Out
        </v-btn>
      </div>
    </div>
  </v-container>
</template>

<style scoped>
.gap-4 {
  gap: 1rem;
}
</style>