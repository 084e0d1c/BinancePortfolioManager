<template>
  <nav
    class="navbar navbar-expand-lg"
    style="background: #42b983; color: black; font-size: 25px"
  >
    <div class="navbar-brand">Binance Portfolio Manager</div>

    <div style="padding-top: 10px;">
      <ul>
        <li class="nav-item active">
          <router-link to="/explore" :style="changePortfolio()"
            >Portfolio</router-link
          >
        </li>
        <li class="nav-item active">
          <router-link to="/settings" :style="changeOptimise()"
            >Optimisation</router-link
          >
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      jwt: localStorage.token,
      showLogout: "",
      portfolio_color: "color: black",
      optimise_color: "color: grey",
    };
  },

  methods: {
    changePortfolio() {
      var currentUrl = window.location.pathname;
      if (currentUrl == "/portfolio") {
        this.portfolio_color = "color: black";
      }
      return this.portfolio_color;
    },
    changeOptimise() {
      var currentUrl = window.location.pathname;
      if (currentUrl == "/optimise") {
        this.optimise_color = "color: black";
      }
      return this.optimise_color;
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
