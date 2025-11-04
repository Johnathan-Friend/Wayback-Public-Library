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
                  @click="reshelve(item.id)"
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
import { onMounted, ref } from 'vue'

const books = ref([])

const headers = [
  { title: 'ID', key: 'id', align: 'start' },
  { title: 'ISBN', key: 'isbn' },
  { title: 'Title', key: 'title' },
  { title: 'DateReturned', key: 'date_returned' },
  { title: 'Actions', key: 'actions', sortable: false },
]

onMounted(() => {
  reset()
})

function reset() {
  books.value = [
    {
      id: 1001,
      isbn: '978-0321765723',
      title: 'The C++ Programming Language',
      date_returned: '2025-10-28',
    },
    {
      id: 1002,
      isbn: '978-0132354181',
      title: 'Clean Code: A Handbook of Agile Software Craftsmanship',
      date_returned: '2025-11-01',
    },
    {
      id: 1003,
      isbn: '978-0262033848',
      title: 'Introduction to Algorithms',
      date_returned: '2025-10-15',
    },
    {
      id: 1004,
      isbn: '978-0134685991',
      title: 'Effective Java',
      date_returned: '2025-10-15',
    },
    {
      id: 1005,
      isbn: '978-0596007126',
      title: 'JavaScript: The Good Parts',
      date_returned: '2025-11-02',
    },
    {
      id: 1006,
      isbn: '978-0135957355',
      title: 'Design Patterns: Elements of Reusable Object-Oriented Software',
      date_returned: '2025-10-15',
    },
    {
      id: 1007,
      isbn: '978-0735619678',
      title: 'Code Complete: A Practical Handbook of Software Construction',
      date_returned: '2025-10-22',
    },
    {
      id: 1008,
      isbn: '978-1449331818',
      title: 'Learning Python, 5th Edition',
      date_returned: '2025-11-03',
    },
    {
      id: 1009,
      isbn: '978-1491904244',
      title: "You Don't Know JS: Up & Going",
      date_returned: '2025-10-30',
    },
    {
      id: 1010,
      isbn: '978-0134494166',
      title: 'Structure and Interpretation of Computer Programs',
      date_returned: '2025-10-15',
    },
    {
      id: 1011,
      isbn: '978-0321125217',
      title: 'Domain-Driven Design: Tackling Complexity in the Heart of Software',
      date_returned: '2025-10-19',
    },
    {
      id: 1012,
      isbn: '978-0201835953',
      title: 'The Mythical Man-Month: Essays on Software Engineering',
      date_returned: '2025-11-04',
    },
    {
      id: 1013,
      isbn: '978-1934356591',
      title: 'The Pragmatic Programmer: From Journeyman to Master',
      date_returned: '2025-10-25',
    },
    {
      id: 1014,
      isbn: '978-0137081073',
      title: 'Working Effectively with Legacy Code',
      date_returned: '2025-10-15',
    },
    {
      id: 1015,
      isbn: '978-1492052203',
      title: 'Database Internals: A Deep Dive into How Distributed Data Systems Work',
      date_returned: '2025-10-29',
    },
    {
      id: 1016,
      isbn: '978-1718501121',
      title: 'Eloquent JavaScript, 3rd Edition',
      date_returned: '2025-11-01',
    },
    {
      id: 1017,
      isbn: '978-0596520687',
      title: 'Head First Design Patterns',
      date_returned: '2025-10-27',
    },
    {
      id: 1018,
      isbn: '978-0132181273',
      title: 'Artificial Intelligence: A Modern Approach',
      date_returned: '2025-10-15',
    },
    {
      id: 1019,
      isbn: '978-0134757599',
      title: 'Deep Learning (Adaptive Computation and Machine Learning series)',
      date_returned: '2025-10-20',
    },
    {
      id: 1020,
      isbn: '978-0321563842',
      title: 'The C Programming Language',
      date_returned: '2025-11-03',
    },
  ]
}

function reshelve(id) {
  const index = books.value.findIndex((book) => book.id === id)
  books.value.splice(index, 1)
}
function reshelveAll() {
  books.value = []
}
</script>
