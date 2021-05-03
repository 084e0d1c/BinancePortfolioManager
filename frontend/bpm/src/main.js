import Vue from "vue";
import App from "./App.vue";
import "../plugins/vue-bootstrap";
import store from "../plugins/store";
import VueRouter from "vue-router";

import Portfolio from "./components/Portfolio.vue";
import Optimise from "./components/Optimise.vue";
import Home from "./components/Home.vue";
import Signup from "./components/Signup.vue";
import Update from "./components/Update.vue";
import About from "./components/About.vue";

Vue.config.productionTip = false;
Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    { path: "/", name: "Home", component: Home },
    { path: "/signup", name: "Signup", component: Signup },
    { path: "/portfolio", name: "Portfolio", component: Portfolio },
    { path: "/optimise", name: "Optimise", component: Optimise },
    { path: "/update", name: "Update", component: Update },
    { path: "/about", name: "About", component: About },
  ],
});

new Vue({
  render: (h) => h(App),
  router,
  store,
}).$mount("#app");
