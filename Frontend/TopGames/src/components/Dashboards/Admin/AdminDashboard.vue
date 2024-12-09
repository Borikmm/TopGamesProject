<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import API from '../../../api/api';
import UserExit from "../../Common/UserExit.vue";

import GamesPanel from "./GamesPanel.vue";

const teachers = ref([]);
const newTeacher = ref({ username: '', password: '' });
const newDiscipline = ref('');
const disciplines = ref([]);
const selectedTeacher = ref(null);
const selectedDisciplines = ref([]);
const activeTab = ref('teachers'); // Вкладка по умолчанию


const showModal = ref(false); // Показывать/скрывать модальное окно
const currentTeacherId = ref(null); // ID текущего преподавателя


// Открытие модального окна
const openModal = (teacherId) => {
  currentTeacherId.value = teacherId;
  const teacher = teachers.value.find((t) => t.id === teacherId);
  selectedDisciplines.value = teacher ? teacher.disciplines.map((d) => d.id) : [];
  showModal.value = true;
};

// Закрытие модального окна
const closeModal = () => {
  showModal.value = false;
  selectedDisciplines.value = [];
};

// Сохранение дисциплин для преподавателя
const saveDisciplines = async () => {
  if (!currentTeacherId.value) {
    alert('Преподаватель не выбран!');
    return;
  }
  try {
    await API.post(`teachers/${currentTeacherId.value}/update_disciplines/`, {
      discipline_ids: selectedDisciplines.value,
    });
    alert('Дисциплины сохранены!');
    closeModal();
    fetchData(); // Обновляем список
  } catch (error) {
    console.error('Ошибка сохранения дисциплин:', error);
  }
};

// Очистка выбранных дисциплин
const clearDisciplines = () => {
  selectedDisciplines.value = [];
};

// Получение преподавателей и дисциплин
const fetchData = async () => {
  try {
    var response = (await API.get('teachers/')).data;
    teachers.value = response;
    console.log('Данные студентов:', response); // Лог данных студентов
    disciplines.value = (await API.get('disciplines/')).data;
  } catch (error) {
    console.error('Ошибка загрузки преподавателей или дисциплин:', error);
  }
};

const assignDisciplines = async (teacherId) => {
  if (!selectedDisciplines.value.length) {
    alert('Выберите дисциплины для преподавателя');
    return;
  }
  try {
    await API.post(`teachers/${teacherId}/update_disciplines/`, {
      discipline_ids: selectedDisciplines.value,
    });
    alert('Дисциплины успешно обновлены');
    fetchData();
  } catch (error) {
    console.error('Ошибка обновления дисциплин:', error);
  }
};

// Добавление нового преподавателя
const addTeacher = async () => {
  if (!newTeacher.value.username || !newTeacher.value.password) {
    alert('Введите логин и пароль преподавателя');
    return;
  }
  try {
    const response = await API.post('teachers/create_teacher/', {
      user: newTeacher.value,
    });
    teachers.value.push(response.data);
    newTeacher.value = { username: '', password: '' };
    alert('Преподаватель добавлен!');
  } catch (error) {
    console.error('Ошибка добавления преподавателя:', error);
    alert('Не удалось добавить преподавателя');
  }
};

// Удаление преподавателя
const deleteTeacher = async (id) => {
  try {
    await API.delete(`teachers/${id}/`);
    teachers.value = teachers.value.filter((teacher) => teacher.id !== id);
    alert('Преподаватель удалён!');
  } catch (error) {
    console.error('Ошибка удаления преподавателя:', error);
  }
};

// Добавление новой дисциплины
const addDiscipline = async () => {
  if (!newDiscipline.value.trim()) {
    alert('Введите название дисциплины');
    return;
  }
  try {
    const response = await API.post('disciplines/', { name: newDiscipline.value });
    disciplines.value.push(response.data);
    newDiscipline.value = '';
    alert('Дисциплина добавлена!');
  } catch (error) {
    console.error('Ошибка добавления дисциплины:', error);
  }
};

// Удаление дисциплины
const deleteDiscipline = async (id) => {
  try {
    await API.delete(`disciplines/${id}/`);
    disciplines.value = disciplines.value.filter((discipline) => discipline.id !== id);
    alert('Дисциплина удалена!');
  } catch (error) {
    console.error('Ошибка удаления дисциплины:', error);
  }
};




onMounted(() => {
  fetchData(); // Если есть функция для загрузки студентов

});
</script>

<template>

  <div class="mainBlock">
    <div class="headerBlock">
      <UserExit />


      <div class="tabs">
        <button :class="{ active: activeTab === 'teachers' }" @click="activeTab = 'teachers'">
          Преподаватели
        </button>
        <button :class="{ active: activeTab === 'disciplines' }" @click="activeTab = 'disciplines'">
          Дисциплины
        </button>
        <button :class="{ active: activeTab === 'games' }" @click="activeTab = 'games'">
          Игры
        </button>
      </div>
    </div>




    <!-- Модальное окно -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h2>Добавление дисциплин</h2>
      <ul>
        <li v-for="discipline in disciplines" :key="discipline.id">
          <label>
            <input type="checkbox" :value="discipline.id" v-model="selectedDisciplines" />
            {{ discipline.name }}
          </label>
        </li>
      </ul>
      <div class="modal-actions">
        <button @click="saveDisciplines">Сохранить</button>
        <button @click="clearDisciplines">Очистить</button>
        <button @click="closeModal">Закрыть</button>
      </div>
    </div>
  </div>

    <div>
      <!-- Навигация между вкладками -->


      <!-- Вкладка "Преподаватели" -->
      <div v-if="activeTab === 'teachers'">
        <h2>Управление преподавателями</h2>
        <form @submit.prevent="addTeacher">
          <input v-model="newTeacher.username" placeholder="Логин преподавателя" required />
          <input v-model="newTeacher.password" type="password" placeholder="Пароль" required />
          <button type="submit">Добавить преподавателя</button>
        </form>

        <table>
          <thead>
            <tr>
              <th>Имя</th>
              <th>Дисциплины</th>
              <th colspan="2">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="teacher in teachers" :key="teacher.id">
              <td>{{ teacher.user_name }}</td>
              <td>{{ teacher.disciplines.map(d => d.name).join(', ') }}</td>
              <td>
                <button @click="deleteTeacher(teacher.id)">Удалить</button>
              </td>
              <td>
                <button @click="openModal(teacher.id)">Добавить дисциплины</button>
              </td>

            </tr>
          </tbody>
        </table>
      </div>

      <!-- Вкладка "Дисциплины" -->
      <div v-if="activeTab === 'disciplines'">
        <h2>Управление дисциплинами</h2>
        <form @submit.prevent="addDiscipline">
          <input v-model="newDiscipline" placeholder="Название дисциплины" required />
          <button type="submit">Добавить дисциплину</button>
        </form>

        <table>
          <thead>
            <tr>
              <th>Название</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="discipline in disciplines" :key="discipline.id">
              <td>{{ discipline.name }}</td>
              <td>
                <button @click="deleteDiscipline(discipline.id)">Удалить</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeTab === 'games'">
          <GamesPanel/>
      </div>


    </div>
  </div>
  
</template>

<style scoped>


.mainBlock{
  height: 500px;
  max-width: 1200px;
}


th{
  text-align: center;
}

.tabs {
  display: flex;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
  justify-content: flex-start;
  border-bottom: 1px solid #ddd;
  background-color: #f9f9f9;
  position: sticky;
  top: 0; /* Вкладки остаются видимыми при прокрутке */
  z-index: 10; /* Чтобы вкладки перекрывали таблицу */
  
}

.tabs button {
  flex: 1; /* Все вкладки занимают одинаковую ширину */
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  border: 1px solid #ddd;
  background: #f9f9f9;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.tabs button.active {
  background: #ddd;
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


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 400px;
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  color: black;
}

.modal-content h2 {
  margin-bottom: 1rem;
}

.modal-content ul {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.modal-content li {
  margin: 0.5rem 0;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-actions button:first-child {
  background: #4caf50;
  color: white;
}

.modal-actions button:nth-child(2) {
  background: #f44336;
  color: white;
}

.modal-actions button:last-child {
  background: #ddd;
}
</style>