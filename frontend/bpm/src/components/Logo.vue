<template>
  <div>
    <div class="row justify-content-center">
      <img
        class="pr-5"
        src="../assets/logo.svg"
        width="15%"
        style="min-width:200px"
      />
    </div>
    <div class="row justify-content-center">
      <h1>{{ headerText }}</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: "Logo",
  props: ["headerText"],
};
</script>
