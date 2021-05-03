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
            platform. Please read this
            <a
              @click="$router.push('/about')"
              style="text-decoration: underline; color: black"
              >link</a
            >
            before proceeding to use the site.
          </p>
          <p class="lead" style="color: black">
            Don't have an account? Click
            <a
              @click="$router.push('/signup')"
              style="text-decoration: underline; color: black"
              >here</a
            >
          </p>
          <p class="lead" style="color: black">
            Updating traded pairs? Click
            <a
              @click="$router.push('/update')"
              style="text-decoration: underline; color: black"
              >here</a
            >
          </p>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row justify-content-center" id="logIn">
        <div class="col-sm-5">
          <div class="form-group">
            <label>UID</label>
            <input
              type="text"
              class="form-control"
              v-model="uid"
              placeholder="User ID"
              v-on:change="getTradedPairs()"
            />
          </div>
          <div v-if="uid">
            <multiselect
              v-model="userTraded"
              :options="userTraded"
              :multiple="true"
              disabled="true"
              placeholder="What you have previously selected"
            ></multiselect>
          </div>
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
        <div class="col-sm-2 mt-2 ">
          <div class="text-center">
            <button
              class="btn btn-dark btn-block"
              @click.prevent="handleSubmit()"
            >
              Let's Go!
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";
import axios from "axios";
import Multiselect from "vue-multiselect";
import "vue-loading-overlay/dist/vue-loading.css";
import {
  DEV,
  GET_ALL_TRADES,
  TRADED_PAIRS,
  CRUD_TRADED_PAIRS,
} from "../config.js";

export default {
  name: "Home",
  props: {},
  components: {
    Loading,
    Multiselect,
  },
  data() {
    return {
      dev: DEV,
      api_key: "",
      api_secret: "",
      assets: [],
      order_history: [],
      userTraded: [],
      uid: "",
    };
  },
  mounted() {
    if (this.dev) {
      this.api_secret = process.env.VUE_APP_API_SECRET;
      this.api_key = process.env.VUE_APP_API_KEY;
    }
    this.getTickers();
    this.userTraded = TRADED_PAIRS;
  },
  methods: {
    handleSubmit() {
      this.loading = true;
      // Fetch the assets here

      this.$store.commit("change_api_details", {
        API_KEY: this.api_key,
        API_SECRET: this.api_secret,
      });
      var json_payload = {
        data: {
          API_KEY: this.api_key,
          API_SECRET: this.api_secret,
          TRADED_PAIRS: this.userTraded,
        },
      };
      axios.post(GET_ALL_TRADES, json_payload).then((res) => {
        this.$store.commit("change_assets", res.data.assets);
        this.$store.commit("change_order_history", res.data.order_history);
        this.$router.push("/portfolio");
      });
    },
    getTradedPairs() {
      var json_payload = {
        uid: this.uid,
        action: "READ",
      };
      axios.post(CRUD_TRADED_PAIRS, json_payload).then((res) => {
        this.userTraded = eval(res.data["Item"]["pairs"]);
      });
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
