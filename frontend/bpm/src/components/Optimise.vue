<template>
  <div>
    <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
    <div class="container" style="margin-top: 25px">
      <div class="row justify-content-center">
        <h3 class="display-10" style="color: black">
          To be implemented soon
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "./NavBar";
export default {
  name: "Optimise",
  data() {
    return {
      loading: false,
    };
  },
  components: {
    NavBar,
  },
};
</script>
