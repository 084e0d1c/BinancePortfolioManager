<template>
  <div>
    <loading :active.sync="loading"></loading>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <div class="col-sm-6 jumbotron" id="header" style="background: #42b983">
          <h1 class="display-5" style="color: black">
            Bianance Portfolio Manager
          </h1>
          <p class="lead" style="color: black">
            In no way or form is this website related to the official binance
            platform. Please click
            <a href="#" target="_blank">here</a> for more information.
          </p>
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <div class="row justify-content-center" id="logIn">
        <div class="col-sm-5">
          <div class="form-group">
            <label>API Secret </label>
            <input
              type="password"
              class="form-control"
              v-model="api_secret"
              placeholder="API Secret"
            />
          </div>
          <div class="form-group">
            <label>API Key </label>
            <input
              type="password"
              class="form-control"
              v-model="api_key"
              placeholder="API Password"
            />
          </div>
        </div>
      </div>
      <br />
      <div class="row justify-content-center">
        <div class="col-sm-2">
          <div class="text-center">
            <button
              class="btn btn-dark btn-block"
              @click.prevent="handleSubmit()"
            >
              Let's Go!
            </button>
          </div>
        </div>
        <div class="col-sm-2">
          <div class="text-center">
            <button class="btn btn-dark btn-block" @click.prevent="gotoDemo()">
              Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import { DEV,DEMO_ASSETS, DEMO_ORDER_HISTORY } from "../config.js";

export default {
  name: "Home",
  props: {},
  components: {
    Loading,
  },
  data() {
    return {
      dev: DEV,
      api_key: "",
      api_secret: "",
      assets: [],
      order_history: [],
    };
  },
  mounted() {
    if (this.dev) {
      this.assets = DEMO_ASSETS;
      this.order_history = DEMO_ORDER_HISTORY;
      this.api_secret = process.env.VUE_APP_API_SECRET;
      this.api_key = process.env.VUE_APP_API_KEY;
    }
  },
  methods: {
    handleSubmit() {
      this.loading = true;
      // Fetch the assets here

      this.$store.commit("change_api_details", {
        API_KEY: this.api_key,
        API_SECRET: this.api_secret,
      });
      this.$store.commit("change_assets", this.assets);
      this.$store.commit("change_order_history", this.order_history);
      this.$router.push("/portfolio");
    },
    gotoDemo() {
      // To be updated later
      this.loading = true;
      this.assets = this.$store.demo_assets;
      this.order_history = this.$store.demo_order_history;
      this.api_key = "";
      this.api_secret = "";
      this.$store.commit("change_demo_status", true);
      this.handleSubmit();
    },
  },
};
</script>
