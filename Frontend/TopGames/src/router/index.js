import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../components/Login.vue'),
    },
    { 
      path: '/admin', 
      name: 'AdminDashboard', 
      component: () => import('../views/AdminDashboardView.vue'),
    },
    { 
      path: '/teacher', 
      name: 'TeacherDashboard', 
      component: () => import('../views/TeacherDashboardView.vue'),
    },
    { 
      path: '/student', 
      name: 'StudentDashboard', 
      component: () => import('../views/StudentDashboardView.vue'),
    },
    {
      path: '/progress/:studentId',
      name: 'StudentProgress',
      component: () => import('../views/StudentProgressDashboardView.vue'),
    },
    {
      path: '/game',
      name: 'GamePage',
      component: () => import('../views/GameDashboardView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');

  if (to.name === 'AdminDashboard' && role !== 'admin') {
    next('/'); // Перенаправляем, если пользователь не админ
  } else if (to.name === 'TeacherDashboard' && role !== 'teacher') {
    next('/'); // Перенаправляем, если пользователь не преподаватель
  } else if (to.name === 'StudentDashboard' && role !== 'student') {
    next('/'); // Перенаправляем, если пользователь не студент
  } else {
    next(); // Доступ разрешён
  }
});

export default router
