<script setup lang="ts">
import { useRouter } from 'vue-router'
import { mdiBookOpenPageVariant } from '@mdi/js'

const router = useRouter();

function goToCheckIn() {
  router.push('/checkin');
}

function goToCheckOut() {
  router.push('/checkout');
}

function goToPatronMembership() {
  router.push('/patron-membership');
}

function goToReshelve() {
  router.push('/reshelve');
}
</script>

<template>
  <v-container
    fluid
    class="d-flex justify-center align-center main-container"
  >
    <v-card
      class="pa-10 text-center elevation-3"
      width="800"
      rounded="xl"
    >
      <v-icon :icon="mdiBookOpenPageVariant" size="72" color="primary" class="mb-6"/>
      <h1 class="mb-8 library-title">Wayback Public Library</h1>
      <div class="d-flex justify-center gap-4">
        <v-btn
          color="secondary"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToCheckOut"
        >
          Check Out
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToCheckIn"
        >
          Check In
        </v-btn>
        <v-btn
          color="purple"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToReshelve"
        >
          Reshelve
        </v-btn>
        <v-btn
          color="purple"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToReshelve"
        >
          Reshelve
        </v-btn>
        <v-btn
          color="orange"
          variant="elevated"
          size="large"
          class="text-white"
          @click="goToPatronMembership"
        >
          Patron Membership
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
