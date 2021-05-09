<template>
  <!-- <form> -->
  <div>
    <loading :active.sync="loading"></loading>
    <div class="container-fluid" style="margin-top: 25px">
      <logo headerText="Generate your login credentials"></logo>
      <div class="row justify-content-center">
        <p class="lead pt-3" style="color: black">
          Already have a unique key? Click
          <a
            @click="$router.push('/')"
            style="text-decoration: underline; color: #42b983"
            >here</a
          >
          to log in!
        </p>
      </div>
      <div class="row justify-content-center mt-2" id="logIn">
        <div class="col-sm-6">
          <h2>What is this?</h2>
          <p>
            The site requires you to key in all pairs that you have previously
            traded in your Binance account. This process can be tedious and
            repetitive.
          </p>
          <p>
            To overcome that, key in your traded pairs only once and use your
            unique generated id to access it. If you need to update it, head
            over to the home page to do so.
          </p>
          <br />
          <h2>How?</h2>
          <ol>
            <li>
              Select the drop down below and choose the pairs that you have
              traded
            </li>
            <li>
              Generate your unique user ID and keep it somewhere safe
            </li>
          </ol>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-sm-6">
          <label class="mt-2">Select pairs that you have traded</label>
          <multiselect
            v-model="userTraded"
            :options="tickers"
            :multiple="true"
            :close-on-select="false"
            placeholder="Selected pairs traded"
          ></multiselect>
          <br />
        </div>
      </div>
      <div class="row justify-content-center" id="signUp">
        <div class="col-sm-6">
          <div class="form-group">
            <label>UID </label>
            <b-input-group class="mt-3">
              <b-form-input
                v-model="uid"
                placeholder="Click Generate"
              ></b-form-input>
              <b-input-group-append>
                <b-button variant="dark" @click.prevent="makeid()"
                  >Generate UID</b-button
                >
              </b-input-group-append>
            </b-input-group>
          </div>

          <div v-if="!uid"></div>
          <div v-else class="alert alert-danger" role="alert">
            Remember to take down your UID, as you will not be able to recover
            it
          </div>
          <div class="text-center mb-5">
            <button
              class="btn btn-dark"
              id="submitButton"
              @click.prevent="signUp()"
            >
              Sign Up
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
import Logo from "./Logo";
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
    Logo,
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
    signUp() {
      this.loading = true;
      if (this.uid == "") {
        alert("Please generate a UID");
        this.loading = false;
        return;
      }
      if (this.userTraded.length == 0) {
        alert("Please ensure you have indicated your pairs traded");
        this.loading = false;
        return;
      }
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
  },
  mounted() {
    this.getTickers();
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
