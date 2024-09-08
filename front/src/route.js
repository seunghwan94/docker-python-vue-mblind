import { createWebHistory, createRouter } from 'vue-router';
import Login from './components/LoginView.vue';
import Main from './components/MainView.vue';

const routes = [
    {
        path: "/chat/login",
        component: Login,
    },{
        path: "/chat/main",
        component: Main,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// router.beforeEach((to, from, next) => {
// const id = sessionStorage.getItem('id');
//     // id가 없고, 로그인 페이지가 아닌 곳으로 가려는 경우 로그인 페이지로 리다이렉트
// if (!id && to.path !== '/login') {
//     next('/login');
// } else {
//     next(); // 그렇지 않으면 원하는 페이지로 이동
// }
// });

export default router;
