<script setup>

import { ref, onMounted } from 'vue';
import API from '../../../api/api';
import router from '../../../router/index';

const newGame = ref({ name: '', file: null, image: null});
const selectedDiscipline = ref(null);
const games = ref([]); // Список игр
const disciplines = ref([]);

// Загрузка файла
const onFileSelected = (event) => {
  const file = event.target.files[0];
  if (file && file.name.endsWith('.zip')) {
    newGame.value.file = file;
  } else {
    alert('Пожалуйста, выберите zip-архив');
  }
};

const onImageSelected = (event) => {
  const file = event.target.files[0];
  if (file && file.name.endsWith('.png')) {
    newGame.value.image = file;
  } else {
    alert('Пожалуйста, выберите png файл');
  }
};

// Добавление новой игры
const addGame = async () => {
  if (!selectedDiscipline.value) {
    alert('Выберите дисциплину!');
    return;
  }
  if (!newGame.value.name.trim() || !newGame.value.file) {
    alert('Введите название игры и выберите файл!');
    return;
  }

  const formData = new FormData();
  formData.append('name', newGame.value.name);
  formData.append('discipline_id', selectedDiscipline.value);
  formData.append('file', newGame.value.file);
  formData.append('image', newGame.value.image);

  try {
    const response = await API.post('games/add/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    games.value.push(response.data); // Добавляем игру в список
    alert('Игра успешно добавлена!');
    newGame.value = { name: '', file: null };
    selectedDiscipline.value = null;
  } catch (error) {
    console.error('Ошибка добавления игры:', error);
    alert('Не удалось добавить игру.');
  }
};

// Удаление игры
const deleteGame = async (gameId) => {
  try {
    await API.delete(`games/${gameId}/`);
    games.value = games.value.filter((game) => game.id !== gameId);
    alert('Игра успешно удалена!');
  } catch (error) {
    console.error('Ошибка удаления игры:', error);
    alert('Не удалось удалить игру.');
  }
};

const checkGame = (game) => {
  // router.push({ 
  //   name: 'GamePage', 
  //   query: { url: `/static/unity-games/${game.name}/index.html` } 
  // });
  window.open(`/static/unity-games/${game.name}/index.html`, '_blank');
};

// Загрузка списка игр
const fetchGames = async () => {
  try {
    games.value = await API.get('games/').then((res) => res.data);
  } catch (error) {
    console.error('Ошибка загрузки списка игр:', error);
  }
};

const fetchDisciplines = async () => {
  try {
    disciplines.value = (await API.get('disciplines/')).data;
  } catch (error) {
    console.error('Ошибка загрузки дисциплин:', error);
  }
};




onMounted(() => {
    fetchGames();
    fetchDisciplines();
});


</script>



<template>

<h2>Управление играми</h2>
<form @submit.prevent="addGame" class="AdditingForm">
    <label>Выберите дисциплину:</label>
    <select v-model="selectedDiscipline">
    <option :value="null">Выберите дисциплину</option>
    <option v-for="discipline in disciplines" :key="discipline.id" :value="discipline.id">
        {{ discipline.name }}
    </option>
    </select>

    <label>Название игры:</label>
    <input v-model="newGame.name" placeholder="Введите название игры" required />

    <label>Картинка для игры:</label>
    <input type="file" @change="onImageSelected" accept=".png" required />

    <label>Загрузите игру (zip):</label>
    <input type="file" @change="onFileSelected" accept=".zip" required />

    <button type="submit">Добавить игру</button>
</form>

<h3>Список игр</h3>
<table>
    <thead>
    <tr>
        <th>Название</th>
        <th>Дисциплина</th>
        <th>Действия</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="game in games" :key="game.id">
        <td>{{ game.name }}</td>
        <td>{{ game.discipline_name }}</td>
        <td>
        <button @click="checkGame(game)">Проверить</button>
        <button @click="deleteGame(game.id)">Удалить</button>
        </td>
    </tr>
    </tbody>
</table>

</template>



<style>


.AdditingForm{
  display: flex;
  align-items: center;
  flex-direction: column;
}

th{
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  table-layout: fixed; /* Фиксирует ширину колонок */
  height: 300px; /* Фиксированная высота таблицы */
  overflow-y: auto; /* Скролл внутри таблицы */

}

table th, table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
}

</style>