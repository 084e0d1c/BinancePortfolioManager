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
    computed_assets: "",
    pieChartData: "",
    max_weight: "",
    coin_with_max_weight: "",
    portfolio_value: "",
    pnlChartDataCategories: "",
    pnlChartDataDataSet1: "",
    pnlChartDataDataSet2: "",
    most_profitable: "",
    least_profitable: "",
    total_pnl: "",
    fusionTable: "",
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
    change_pie_chart_data(state, payload) {
      state.pieChartData = payload["pieChartData"];
      state.computed_assets = payload["computed_assets"];
      state.max_weight = payload["max_weight"];
      state.coin_with_max_weight = payload["coin_with_max_weight"];
      state.portfolio_value = payload["portfolio_value"];
    },
    change_pnl_data(state, payload) {
      state.pnlChartDataCategories = payload["pnlChartDataCategories"];
      state.pnlChartDataDataSet1 = payload["pnlChartDataDataSet1"];
      state.pnlChartDataDataSet2 = payload["pnlChartDataDataSet2"];
      state.most_profitable = payload["most_profitable"];
      state.least_profitable = payload["least_profitable"];
      state.total_pnl = payload["total_pnl"];
    },
    change_historical_position_data(state, payload) {
      state.fusionTable = payload;
    },
    change_portfolio_accessed_before(state,payload) {
      state.portfolio_accessed_before = payload;
    }
  },
  actions: {},
});
