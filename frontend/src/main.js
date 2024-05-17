import  { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Correct path to the router instance
import './assets/style.css'

createApp(App).use(router).mount('#app')