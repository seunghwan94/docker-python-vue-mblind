import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App);

app.config.globalProperties.$BackURL = 'http://localhost:3000/';

app.use(router).mount('#app');
