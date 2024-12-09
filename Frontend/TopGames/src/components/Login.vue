<script setup>
import { ref } from 'vue';
import API from '../api/api';
import router from '../router/index';
import { onMounted } from 'vue';

const username = ref('');
const password = ref('');
const loginError = ref('');


const isErrorPass = ref(false);
const isErrorUser = ref(false);

const checkAuth = () => {
  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');

  if (token && role) {
    // Перенаправляем пользователя на его личный кабинет
    if (role === 'admin') {
      router.push('/admin');
    } else if (role === 'teacher') {
      router.push('/teacher');
    } else if (role === 'student') {
      router.push('/student');
    }
  }
};

// Проверяем аутентификацию при загрузке страницы
onMounted(() => {
  checkAuth();
});

const login = async () => {
  try {
    var need = false;
    if (password.value.trim() === '')
    {
      isErrorPass.value = true;
      need = true;
    }
    if (username.value.trim() === '')
    {
      isErrorUser.value = true;
      need = true;
    }
    if (need)
    {
      return;
    }


    const response = await API.post('token/', { username: username.value, password: password.value });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);

    // Получаем роль пользователя
    const userResponse = await API.get('current-user/');
    localStorage.setItem('user_role', userResponse.data.role);


    alert('Успешный вход!');

    if (userResponse.data.role == "admin")
    {
      router.push('/admin');
    }
    else if (userResponse.data.role == "teacher")
    {
      router.push('/teacher');
    }
    else if (userResponse.data.role == "student")
    {
      router.push('/student');
    }

  } catch (error) {
    if (error.status === 401)
    {
      loginError.value = "Такого пользователя не существует!";
    }

  }
};
</script>

<template>
  <div>
    <h1>Вход</h1>
    <form @submit.prevent="login">
      <input :class="{'error': isErrorUser}"  v-model="username" placeholder="Логин" />
      <input :class="{'error': isErrorPass}"  v-model="password" type="password" placeholder="Пароль" />
      <button type="submit">Войти</button>
    </form>
    <p v-if="loginError">{{ loginError }}</p>
  </div>
</template>



<style scoped>
/* Общий стиль для всей страницы */
div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Полная высота экрана */
  width: 100vw; /* Полная ширина экрана */
  background: linear-gradient(135deg, #72c3f9, #11649c, #44b3ff);
  background-size: 400% 400%;
  animation: gradient-animation 6s ease infinite;
  overflow: hidden; /* Убираем скролл */
}

/* Стили для заголовка */
h1 {
  color: #add8e6; /* Нежно-голубой цвет */
  font-family: 'Poppins', sans-serif; /* Красивый шрифт */
  font-size: 6rem; /* Размер заголовка для ПК */
  margin-bottom: 10px; /* Уменьшаем расстояние между заголовком и формой */
  text-align: center;
  text-transform: uppercase; /* Делаем все буквы заглавными */
  font-weight: 700; /* Более жирный шрифт */
  position: absolute; /* Фиксируем заголовок */
  top: 5%; /* Делаем его еще выше */
  left: 50%; /* Центрируем заголовок по горизонтали */
  transform: translateX(-50%); /* Центрируем по горизонтали */
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.3); /* Тень для заголовка */
  animation: fadeIn 2s ease-in-out; /* Плавное появление заголовка */
}

/* Плавная анимация для заголовка */
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

/* Стили для формы */
form {
  display: flex;
  flex-direction: column;
  width: 100%; /* Форма займет всю ширину доступного пространства */
  max-width: 900px; /* Максимальная ширина формы для ПК */
  padding: 60px;
  background-color: rgba(255, 255, 255, 0.85);
  border-radius: 25px; /* Более закругленные углы */
  box-shadow: 0 4px 50px rgba(0, 0, 0, 0.2); /* Более выраженная тень */
  position: relative; /* Сделаем позицию относительно родительского контейнера */
  top: 20%; /* Сделаем форму ближе к верхней части экрана */
  animation: slideIn 2s ease-out; /* Плавное появление формы */
}

/* Плавная анимация для формы */
@keyframes slideIn {
  0% { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* Стили для полей ввода */
input {
  padding: 20px;
  margin-bottom: 25px;
  border-radius: 12px;
  border: 2px solid #9e9e9e;
  font-size: 1.2rem;
  outline: none;
  transition: all 0.3s ease;
}


.error{
  border: 2px solid #f61616;
}

input:focus {
  border-color: #44b3ff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.6); /* Синий эффект при фокусе */
}

/* Стили для кнопки */
button {
  padding: 20px;
  background-color: #44b3ff;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.4rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease;
}

button:hover {
  background-color: #56aee3;
  transform: scale(1.05); /* Легкое увеличение кнопки при наведении */
}

/* Стили для ошибки */
p {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
  font-size: 1.2rem;
  position: fixed;
  top: 38%;
}

/* Анимация для фона */
@keyframes gradient-animation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

</style>