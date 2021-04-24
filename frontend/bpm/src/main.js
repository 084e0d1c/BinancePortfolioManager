import Vue from "vue";
import App from "./App.vue";
import "../plugins/vue-bootstrap";
import store from "../plugins/store";
import VueRouter from "vue-router";

import Portfolio from "./components/Portfolio.vue";
import Home from "./components/Home.vue";

Vue.config.productionTip = false;
Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    { path: "/", name: "Home", component: Home },
    { path: "/portfolio", name: "Portfolio", component: Portfolio },
  ],
});

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount("#app");
