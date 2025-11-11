<template>
  <v-container fluid class="fill-height pa-4">
    <v-row class="h-100" justify="center" align="center">
      <v-col cols="auto">
        <v-sheet border rounded style="min-width: 800px">
          <v-data-table :headers="headers" :hide-default-footer="books.length < 11" :items="books">
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title> Reshelve Bin Items </v-toolbar-title>

                <v-spacer></v-spacer>

                <v-btn
                  class="me-2"
                  rounded="lg"
                  text="Reshelve All"
                  border
                  @click="reshelveAll"
                ></v-btn>
              </v-toolbar>
            </template>
            <template v-slot:item.actions="{ item }">
              <div class="d-flex">
                <v-btn
                  class="me-2"
                  rounded="lg"
                  text="Reshelve"
                  border
                  @click="reshelve(item.ItemID)"
                  align="end"
                ></v-btn>
              </div>
            </template>
          </v-data-table>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import api from '../api/api'
import { onMounted, ref } from 'vue'

const books = ref([])

const headers = [
  { title: 'ID', key: 'ItemID', align: 'start' },
  { title: 'ISBN', key: 'ISBN' },
  { title: 'Actions', key: 'actions', sortable: false },
]

onMounted(() => {
  reset()
})

async function reset() {
  books.value = await api.getItemsNeedingReshelving()
  console.log(books)
}

async function reshelve(id) {
  await api.reshelveItem(id)
  books.value = books.value.filter((book) => book.ItemID !== id)
}
async function reshelveAll() {
  for (const book of books.value) {
    await reshelve(book.ItemID)
  }
  books.value = books.value.filter((book) => book.ItemID !== id)
}
</script>
