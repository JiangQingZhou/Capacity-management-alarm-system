import { createRouter, createWebHistory } from 'vue-router'
import Example from '../views/Example.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'example',
            component: Example,
            redirect: '/one',
            children: [
                {
                    path: 'one',
                    name: 'One',
                    component: () => import('@/components/charts/ChartOne.vue')
                },
                {
                    path: 'two',
                    name: 'Two',
                    component: () => import('@/components/charts/ChartTwo.vue')
                }
            ],
        }
    ],
})

export default router
