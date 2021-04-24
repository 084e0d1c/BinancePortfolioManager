<template>
  <div>
    <TopBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <div class="col-sm-8 jumbotron" id="header" style="background: #42b983">
          <h1 class="display-5" style="color: black">
            Welcome to BPM!
          </h1>
          <p class="lead" style="color: black">
            In no way or form is this website related to the official binance
            platform. Please click
            <a href="#" target="_blank">here</a> for more information.
          </p>
        </div>
      </div>
    </div>
    <div class="row justify-content-center" id="logIn">
      <div class="col-sm-6">
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
        <br />
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
</template>

<script>
// import Loading from "vue-loading-overlay";
import TopBar from "./TopBar";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "Home",
  props: {},
  components: {
    TopBar,
    Loading,
  },
  data() {
    return {
      api_key: "",
      api_secret: "",
      dummy_asset: [
        { Coin: "ALGO", Quantity: 256.46999999999997, Price: "1.25550000" },
        { Coin: "BNB", Quantity: 0.772, Price: "546.90940000" },
        { Coin: "BTC", Quantity: 0.0112718, Price: "53375.84000000" },
        { Coin: "DOT", Quantity: 6.23, Price: "34.93220000" },
        { Coin: "EGLD", Quantity: 1.589, Price: "175.50000000" },
        { Coin: "ETH", Quantity: 0.20609000000000005, Price: "2553.28000000" },
        { Coin: "USDT", Quantity: 1.0215684, Price: 1 },
        { Coin: "ZIL", Quantity: 1371.4, Price: "0.18100000" },
      ],
    };
  },
  methods: {
    handleSubmit() {
      this.loading = true;
      // Fetch the assets here

      this.$store.commit("change_api_details", {
        API_KEY: this.api_key,
        API_SECRET: this.api_secret,
      });
      this.$store.commit("change_assets", this.dummy_asset);
      this.$router.push("/portfolio");
    },
  },
};
</script>
