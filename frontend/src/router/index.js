import {createRouter, createWebHistory} from 'vue-router'
import Online from "@/components/Online.vue";
import Alerts from "@/components/Alerts.vue";
import Stats from "@/components/Stats.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Online,
        },
        {
            path: '/alerts',
            name: 'alerts',
            component: Alerts,
        },
        {
            path: '/stats',
            name: 'stats',
            component: Stats,
        }
    ],
})

export default router
