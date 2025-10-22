<script setup>
    import { ref } from 'vue';
    import axios from 'axios'

    const students = ref([])
    const error = ref(null)

    async function getData() {
        try {
            const response = await axios.get('https://fastapi.twnsnd.net/students')
            students.value = response.data
        } catch (err) {
            error.value = err.message
            console.error('Error fetching students:', err)
        }
    }
</script>

<template>
  <main>
    <p>Click this button to query database through: https://fastapi.twnsnd.net/students</p>
    <p>this returns a list of students from students table</p>
    <button  v-on:click="getData">Click Me to get data</button>
    <div v-if="error">Error: {{ error }}</div>
    <ul v-else>
      <li v-for="student in students" :key="student.id">
        {{ student.first_name + ' ' + student.last_name }}
      </li>
    </ul>
  </main>
</template>