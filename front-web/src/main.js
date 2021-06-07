import './styles.css';

import {createApp} from 'vue';
import App from '@/App.vue';

import {NotificationManager} from "@/modules/notifications";

const app = createApp(App);
app.use(NotificationManager);

app.config.globalProperties.$appConfig = window.__ENV__;

app.mount('#app');
