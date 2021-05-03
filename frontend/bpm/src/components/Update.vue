<template>
  <!-- <form> -->
  <div>
    <loading :active.sync="loading"></loading>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <div class="col-sm-6 jumbotron" id="header" style="background: #42b983">
          <h1 class="display-5" style="color: black">
            Update your traded pairs
          </h1>
        </div>
      </div>
      <div class="row justify-content-center" id="signUp">
        <div class="col-sm-6">
          <div class="form-group">
            <label>UID</label>
            <input
              type="text"
              v-model="uid"
              class="form-control"
              name="Name"
              id="Name"
              placeholder="Enter your UID"
              v-on:change="getTradedPairs()"
            />
          </div>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-sm-6">
          <label>Update pairs that you have traded</label>
          <multiselect
            v-model="userTraded"
            :options="tickers"
            :multiple="true"
            :close-on-select="false"
            placeholder="Selected pairs traded"
          ></multiselect>
          <br />
          <div class="text-center">
            <button
              class="btn btn-dark"
              id="submitButton"
              @click.prevent="updateTradedPairs()"
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- </form> -->
</template>

<script>
import axios from "axios";
// Import component
import Loading from "vue-loading-overlay";
import Multiselect from "vue-multiselect";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";
import { GET_TICKERS, CRUD_TRADED_PAIRS } from "../config.js";

export default {
  name: "Signup",
  data() {
    return {
      uid: "",
      loading: false,
      userTraded: [],
      tickers: [],
    };
  },

  components: {
    Loading,
    Multiselect,
  },

  methods: {
    // to refresh the navbar
    makeid() {
      var result = [];
      var characters =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";
      var charactersLength = characters.length;
      for (var i = 0; i < 25; i++) {
        result.push(
          characters.charAt(Math.floor(Math.random() * charactersLength))
        );
      }
      this.uid = result.join("");
    },
    updateTradedPairs() {
      this.loading = true;
      var json_payload = {
        uid: this.uid,
        pairs: this.userTraded,
        action: "WRITE",
      };
      axios.post(CRUD_TRADED_PAIRS, json_payload).then((res) => {
        alert("Successfully saved pairs", res.data);
        this.$router.push("/");
      });
    },
    getTickers() {
      axios.get(GET_TICKERS).then((res) => {
        this.tickers = res.data;
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
  mounted() {
    this.getTickers();
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
