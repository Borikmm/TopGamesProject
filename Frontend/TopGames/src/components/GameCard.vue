<template>
    <div class="game-card" @click="emitClick">
      <div class="game-image">
        <img :src="game.image_url" alt="game image" />
      </div>
      <div class="game-info">
        <h3>{{ game.name }}</h3>
        <p>{{ game.discipline_name }}</p>
      </div>
    </div>
  </template>
  
<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  game: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['click']);

const emitClick = () => {
  emit('click');
};
</script>
  
<style scoped>

  p, h3{
    color: black;
  }
  .game-card {
    width: 200px;
    height: 300px;
    perspective: 1000px;
    cursor: pointer;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateZ(0);
    transition: transform 0.3s ease;
  }
  
  .game-card:hover {
    transform: rotateY(10deg) rotateX(5deg) scale(1.05);
  }
  
  .game-image img {
    width: 100%;
    height: 150px;
    border-radius: 8px 8px 0 0;
    object-fit: cover;
  }
  
  .game-info {
    padding: 1rem;
    text-align: center;
  }
  
  .game-info h3 {
    margin: 0;
    font-size: 1.2rem;
  }
  
  .game-info p {
    margin: 0.5rem 0 0;
    font-size: 0.9rem;
    color: #666;
  }
  </style>