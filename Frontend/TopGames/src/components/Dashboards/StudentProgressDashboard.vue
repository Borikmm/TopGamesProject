<script lang="ts" setup>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';


const route = useRoute();
const router = useRouter();
const studentId = route.params.studentId;

// Заглушка для отображения прогресса
onMounted(() => {
  console.log(`Показать прогресс студента с ID ${studentId}`);
});

const goBack = () => {
  router.push('/teacher');
};
</script>

<template>

  <div>
    <h1>Прогресс студента</h1>
    <p>Здесь будет информация о прогрессе студента с ID {{ studentId }}</p>
    <button @click="goBack">Назад</button>
  </div>
</template>