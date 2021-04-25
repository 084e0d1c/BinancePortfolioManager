// https://www.smashingmagazine.com/2020/01/data-components-vue-js/

import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    api_details: {
      key: "#",
      secret: "#",
    },
    assets: {},
    order_history: [],
    demo_status: false,
  },
  getters: {},
  mutations: {
    change_api_details(state, payload) {
      state.api_details.key = payload["API_KEY"];
      state.api_details.secret = payload["API_SECRET"];
    },
    change_assets(state, payload) {
      state.assets = payload;
    },
    change_order_history(state, payload) {
      state.order_history = payload;
    },
    change_demo_status(state,payload) {
      state.demo_status = payload;
    }
  },
  actions: {},
});
