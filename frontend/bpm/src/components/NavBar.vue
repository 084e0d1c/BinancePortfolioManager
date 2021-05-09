<template>
  <nav
    class="navbar navbar-expand-lg"
    style="background: #4cba88; color: black; font-size: 25px"
  >
    <img
      class="pr-2"
      src="../assets/logo.svg"
      width="4%"
      style="min-width:25px"
    />
    <div class="navbar-brand">Binance Portfolio Manager</div>

    <div style="padding-top: 10px;">
      <ul>
        <li class="nav-item active">
          <router-link to="/portfolio" :style="changePortfolio()"
            >Portfolio</router-link
          >
        </li>
        <li class="nav-item active">
          <router-link to="/optimise" :style="changeOptimise()"
            >Optimisation</router-link
          >
        </li>
      </ul>
    </div>
    <div class="justify-content-right">
      <li class="nav-item">
        <button type="button" class="btn btn-dark" @click="logOut()">
          Logout
        </button>
      </li>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      portfolio_color: "color: black",
      optimise_color: "color: grey",
    };
  },

  methods: {
    changePortfolio() {
      var currentUrl = window.location.pathname;
      if (currentUrl == "/portfolio") {
        this.portfolio_color = "color: black";
        this.optimise_color = "color: grey";
      }
      return this.portfolio_color;
    },
    changeOptimise() {
      var currentUrl = window.location.pathname;
      if (currentUrl == "/optimise") {
        this.optimise_color = "color: black";
        this.portfolio_color = "color: grey";
      }
      return this.optimise_color;
    },
    logOut() {
      this.$store.commit("reset_state");
      this.$router.push("/");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
  font-size: 20px;
}
a {
  color: #42b983;
}
</style>
