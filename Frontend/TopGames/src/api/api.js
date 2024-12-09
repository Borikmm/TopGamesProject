import axios from 'axios';
import router from '../router/index';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

// Добавление access_token в заголовки
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехват ответов для проверки истечения токена
API.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Проверяем, если ошибка связана с истечением токена
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Обновляем токен
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('Refresh token отсутствует');
        }

        const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
          refresh: refreshToken,
        });

        // Сохраняем новый access_token
        localStorage.setItem('access_token', response.data.access);

        // Повторяем оригинальный запрос с новым токеном
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return API(originalRequest);
      } catch (refreshError) {
        console.error('Ошибка обновления токена:', refreshError);

        // Удаляем токены и перенаправляем на страницу входа
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_role');
        router.push('/login');
      }
    }

    return Promise.reject(error);
  }
);

export default API;