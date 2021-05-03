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
            About this website
          </p>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row justify-content-center" id="logIn">
        <div class="col-sm-5">
          <h2>What data is collected</h2>
          <p>
            On this site, we do not collect any of your data. The logging in
            function implemented is merely a way to provide a better user
            experience, so that you do not have to manually enter your traded
            pairs each time.
          </p>
          <p>
            Your trade history is constructed using your API credentials. Once
            you leave the site, everything is removed.
          </p>
          <br />
          <h2>Quality of data</h2>
          <p>
            Price data is retrieved from Binance and stored on AWS cloud. Prices
            are fetched every hour and hence you may experience some
            discrepencies in your portfolio value.
          </p>

          <p>
            There are limitations, as Binance API does not allow users to easily
            track their portfolio holdings, deposits, referral income or even
            staking rewards. Hence, I have made some assumptions when building
            this page.
          </p>
          <br />
          <h2>Assumptions</h2>
          <ol>
            <li>
              Binance is the only exchange that you use to make your trades
            </li>
            <li>
              Your portfolio holdings are constructed using your historical
              trades
            </li>
            <li>
              Referral, staking and external deposits will not be included in
              portfolio value until you have executed a trade with that new
              value
            </li>
            <li>
              Margin trading P&L is not included
            </li>
          </ol>
          <br />
          <h2>How to obtain Binance API Key and Secret</h2>
          <p>
            Refer to
            <a href="https://www.binance.com/en/support/articles/360002502072"
              >Binance's official support documentation</a
            >
            on how to do it. Ensure that when generating the key
            <b>the trading functions are disbaled</b>.
          </p>
        </div>
      </div>
      <br />
      <div class="row justify-content-center">
        <div class="col-sm-2 mt-2 ">
          <div class="text-center">
            <button class="btn btn-dark btn-block" @click.prevent="gotoHome()">
              I understand the limitations
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "About",
  methods: {
    gotoHome() {
      this.$router.push("/");
    },
  },
};
</script>
