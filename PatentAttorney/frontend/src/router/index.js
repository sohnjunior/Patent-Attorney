import Vue from 'vue'
import VueRouter from 'vue-router'
import PredictApp from "../views/PredictApp.vue";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'PredictApp',
    component: PredictApp
  },
]

const router = new VueRouter({
  routes
})

export default router
