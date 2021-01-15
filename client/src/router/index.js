import Vue from 'vue';
import VueRouter from 'vue-router';
import HomePage from '../views/HomePage.vue';
import PredictPage from "../views/PredictPage.vue";
import Store from '../store/index';

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage,
      beforeEnter: (to, from, next) => {
        if(from.name === 'predict') {
          Store.commit('initData');
        }
        next();
      }
    },
    {
      path: '/predict',
      name: 'predict',
      component: PredictPage
    }
  ]
})

export default router
