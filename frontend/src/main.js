import './styles.css'
import './tailwindstyles.css';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueAxios from 'vue-axios'
import axios from './api/axios'
import mitt from 'mitt';

const app = createApp(App);

const eventBus = mitt();
app.provide('eventBus', eventBus);
app.use(VueAxios, axios);
app.use(router)
app.mount('#app')
