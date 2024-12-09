<script setup>
import { ref, onMounted } from 'vue';
import API from '../../api/api';

import GameCard from "../GameCard.vue";

import UserExit from "../Common/UserExit.vue";

const studentLogin = ref(''); // Логин ученика
const games = ref([]); // Список игр

const handleGameClick = (game) => {
  window.open(`/static/unity-games/${game.name}/index.html`, '_blank');
};

// Загрузка данных ученика и игр
const fetchStudentData = async () => {
  try {
    const studentData = await API.get('current-student/');
    studentLogin.value = studentData.data.user_name; // Логин ученика
    games.value = studentData.data.games || [];
  } catch (error) {
    console.error('Ошибка загрузки данных ученика или игр:', error);
  }
};

onMounted(fetchStudentData);
</script>

<template>

  <div class="student-dashboard">
    
    <!-- Логин ученика -->
    <header class="header">
      <div style="position: fixed; left: 200px;">
        <UserExit />
      </div>
      <div>
        <h1>Привет, {{ studentLogin }}!</h1>
      </div>


      
    </header>

    <!-- Список игр -->
    <section class="games-section">

      <h2>Доступные игры:</h2>
      <div v-if="games.length === 0" class="no-games">
        <p>Тут ничего нет</p>
      </div>
      <div v-else class="games-container">
        <div class="games-list">
          <GameCard
            v-for="game in games"
            :key="game.id"
            :game="game"
            @click="handleGameClick(game)"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.student-dashboard {
  display: flex;
  font-family: Arial, sans-serif;
  background-color: wheat;
  flex-direction: column;
  flex-wrap: nowrap;
  align-items: center;
  height: 740px;
  width: 1200px;
}

.header {
  display: flex;
  justify-content: center;
  padding: 1rem;
  background: linear-gradient(to right, rgb(249, 33, 33), rgb(253, 82, 110));;
  color: black;
  width: 100%;
  align-items: center;

}

.header h1 {
  margin: 0;
  font-size: 2.2rem;
}
.games-section h2 {
  margin: 0;
  font-size: 1.5rem;
  color: black;
}

.games-section {
  margin: 1rem;
  margin-top: 120px;
}

.games-container {
  overflow-x: auto;
  display: flex;
  flex-wrap: nowrap; /* Запрещаем перенос элементов */
  gap: 1rem;
  padding: 1rem 0;
  scroll-snap-type: x mandatory; /* Для снаппинга карточек */
  scroll-behavior: smooth; /* Плавная прокрутка */
}

.games-container::-webkit-scrollbar {
  height: 8px; /* Горизонтальный скроллбар */
}

.games-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

.games-container::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

.games-list {
  display: flex;
  flex-wrap: nowrap; /* Запрещаем перенос */
  gap: 1rem; /* Расстояние между карточками */
}

.no-games {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.2rem;
  color: #888;
}
</style>