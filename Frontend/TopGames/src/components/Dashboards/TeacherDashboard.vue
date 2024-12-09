<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import API from '../../api/api';
import { useRouter } from 'vue-router';
import UserExit from "../Common/UserExit.vue";

const disciplines = ref([]); // Дисциплины преподавателя
const students = ref([]); // Список студентов
const showModal = ref(false); // Отображение модального окна
const selectedStudentId = ref(null); // ID текущего студента
const selectedDisciplines = ref([]); // Дисциплины для назначения студенту
const newStudent = ref({ username: '', password: '' });
const router = useRouter();
const teacherData = ref(null);
const teacherName = ref('');

// Загрузка данных преподавателя
const fetchDisciplines = async () => {
  try {
    disciplines.value = (await API.get('teachers/my_disciplines/')).data;
  } catch (error) {
    console.error('Ошибка загрузки данных дисциплин:', error);
  }
};

const fetchStudents = async () => {
  try {
    const response = await API.get('teachers/my_students/');
    students.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки студентов:', error);
  }
};

// Загрузка данных преподавателя
const fetchTeacher = async () => {
  try {
    teacherData.value = (await API.get('teachers/current_teacher/')).data;
    teacherName.value = teacherData.value.username;
  } catch (error) {
    console.error('Ошибка загрузки данных учителя:', error);
  }
};

// Открытие модального окна для назначения дисциплин
const openModal = (studentId, currentDisciplines) => {
  selectedStudentId.value = studentId;
  selectedDisciplines.value = currentDisciplines.map((d) => d.id); // Загружаем текущие дисциплины
  showModal.value = true;
};

// Закрытие модального окна
const closeModal = () => {
  selectedStudentId.value = null;
  selectedDisciplines.value = [];
  showModal.value = false;
};

// Сохранение дисциплин для студента
const saveDisciplines = async () => {
  if (!selectedStudentId.value) {
    alert('Студент не выбран!');
    return;
  }
  try {
      // Удаляем undefined из списка дисциплин
    selectedDisciplines.value = selectedDisciplines.value.filter((id) => id !== undefined);
    await API.post(`students/${selectedStudentId.value}/update_disciplines/`, {
      discipline_ids: selectedDisciplines.value,
    });
    alert('Дисциплины обновлены');
    closeModal();
    fetchDisciplines();
    fetchStudents();
  } catch (error) {
    console.error('Ошибка обновления дисциплин:', error);
  }
};

// Удаление студента
const deleteStudent = async (studentId) => {
  try {
    await API.delete(`students/${studentId}/`);
    students.value = students.value.filter((s) => s.id !== studentId);
    alert('Студент удалён!');
  } catch (error) {
    console.error('Ошибка удаления студента:', error);
  }
};


// Добавление нового ученика
const addStudent = async () => {
  try {
    const response = await API.post('students/create_student/', { 
      user: newStudent.value ,
      teacher_id: teacherData.value.id
    });
    students.value.push(response.data);
    newStudent.value = { username: '', password: '' };
    alert('Ученик добавлен!');
  } catch (error) {
    console.error('Ошибка добавления ученика:', error);
    alert('Не удалось добавить ученика');
  }
};

// Переход на страницу прогресса студента
const goToProgress = (studentId) => {
  router.push(`/progress/${studentId}`);
};

// Возврат на главную страницу преподавателя
const goBack = () => {
  router.push('/teacher');
};

onMounted(() => {

  fetchStudents(); // Если есть функция для загрузки студентов
  fetchDisciplines();
  fetchTeacher(); // Если есть функция для загрузки студентов
});

</script>

<template>
  <UserExit />
  <div>
    <h1>Личный кабинет преподавателя {{ teacherName }}</h1>

    <!-- Список дисциплин -->
    <div>
      <h2>Мои дисциплины</h2>
      <ul>
        <li v-for="discipline in disciplines" :key="discipline.id">
          {{ discipline.name }}
        </li>
      </ul>
    </div>

    <!-- Список студентов -->
    <div>
      <div>
        <h2>Добавить ученика</h2>
        <form @submit.prevent="addStudent">
          <input v-model="newStudent.username" placeholder="Логин ученика" required />
          <input v-model="newStudent.password" placeholder="Пароль" type="password" required />
          <button type="submit">Добавить</button>
        </form>
      </div>


      <h2>Список студентов</h2>
      <table>
        <thead>
          <tr>
            <th>Логин</th>
            <th>Дисциплины</th>
            <th>Команды</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.id">
            <td>{{ student.user_name }}</td>
            <td>{{ student.disciplines.map(d => d.name).join(', ') }}</td>
            <td>
              <button @click="openModal(student.id, student.disciplines)">Назначить дисциплины</button>
              <button @click="deleteStudent(student.id)">Удалить</button>
              <!-- <button @click="goToProgress(student.id)">Прогресс</button> -->
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Назначить дисциплины</h2>
        <ul>
          <li v-for="discipline in disciplines" :key="discipline.id">
            <label>
              <input
                type="checkbox"
                :value="discipline.id"
                v-model="selectedDisciplines"
              />
              {{ discipline.name }}
            </label>
          </li>
        </ul>
        <div class="modal-actions">
          <button @click="saveDisciplines">Сохранить</button>
          <button @click="closeModal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>


<style>



h1{
  font-size: 2.5rem;
}

h2{
  font-size: 2rem;
}

li{
  font-size: 1.8rem;
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
  color: black;
}

.modal-content {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  width: 400px;
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

</style>