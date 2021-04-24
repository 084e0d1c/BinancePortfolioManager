<template>
  <nav
    class="navbar navbar-expand-lg"
    style="
      background: #42b983;
      color: black;
      font-size: 25px;
      padding-top: 10px;
    "
  >
    <div class="navbar-brand">Binance Portfolio Manager</div>
  </nav>
</template>

<script>
export default {
  name: "TopBar",
  data() {
    return {
      jwt: localStorage.token,
      showLogout: "",
    };
  },
  created() {
    if (localStorage.token) {
      this.showLogout = true;
    } else {
      this.showLogout = false;
    }
  },
  methods: {
    logOut() {
      if (localStorage.token) {
        localStorage.removeItem("token");
        this.showLogout = false;
      }
      this.$router.push("/");
    },

    checkJWT: function () {
      setInterval(function () {
        if (!localStorage.token) {
          return false;
        } else {
          return true;
        }
      }, 1);
    },
  },
  watch: {
    jwt() {
      // console.log(this.jwt);
      // console.log(this.showLogout);
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
}
a {
  color: #42b983;
}
</style>
