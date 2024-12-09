<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const gameUrl = ref('');

onMounted(() => {
  // Получаем URL игры из параметра маршрута
  gameUrl.value = route.query.url || '';
});
</script>

<template>
  <div class="game-page">
    <h1>Игра</h1>
    <div v-if="gameUrl">
      <!-- Путь игры напрямую к серверу Django -->
      <iframe
        :src="gameUrl"
        width="100%"
        height="600px"
        frameborder="0"
        allowfullscreen
      ></iframe>
    </div>
    <div v-else>
      <p>URL игры не указан или недоступен</p>
    </div>
  </div>
</template>

<style scoped>
.game-page {
  text-align: center;
}

iframe {
  border: none;
}
</style>