<script lang="ts" setup>

import router from '../router/index';


</script>

<template>
  <div class="home-page">
    <header class="hero">
      <h1>Добро пожаловать на EduGames!</h1>
      <p>
        Здесь вы найдете образовательные мини-игры, которые сделают обучение увлекательным.
        Администраторы, преподаватели и ученики — у каждого есть свои возможности!
      </p>
    </header>

    <main>
      <button @click="router.push('/login')" class="login-button">
        Войти
      </button>
    </main>
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 0 20px;
  text-align: center;
  color: #ffffff;
}

.hero {
  max-width: 600px;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 2.8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  line-height: 1.2;
  color: #e0f7fa;
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.hero p {
  font-size: 1.3rem;
  color: #cfd8dc;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.login-button {
  padding: 0.8rem 2.5rem;
  font-size: 1.2rem;
  font-weight: 500;
  color: #ffffff;
  background-color: #00b894;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.login-button:hover {
  background-color: #55efc4;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.login-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>