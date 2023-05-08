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
        },
        {
            path: '/about',
            name: 'about',
            // route level code-splitting
            // this generates a separate chunk (About.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import('../views/AboutView.vue'),
        },
    ],
})

export default router
