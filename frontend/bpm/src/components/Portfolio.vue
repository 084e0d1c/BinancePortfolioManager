<template>
  <div>
    <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
    <div>{{ api_key }} {{ api_key }}</div>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <h3 class="display-10" style="color: black">
          Historical Net Asset Value
        </h3>
      </div>
      <h3 class="display-10" style="color: black"></h3>
      <div class="row justify-content-center">
        <div class="col-sm-12" id="header">
          <timeSeriesChart
            type="timeseries"
            width="100%"
            height="600"
            dataFormat="json"
            :dataSource="timeSeriesData"
          >
          </timeSeriesChart>
        </div>
      </div>
    </div>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <h3 class="display-10" style="color: black">
          Portfolio Contribution
        </h3>
      </div>
      <div class="row justify-content-center">
        <div class="col-sm-6" id="header">
          <pnlChart
            type="stackedcolumn2d"
            width="100%"
            height="600"
            dataFormat="json"
            :dataSource="pnlChartData"
          >
          </pnlChart>
        </div>
        <div class="col-sm-6" id="header">
          <pieChart
            type="pie3d"
            width="100%"
            height="600"
            dataFormat="json"
            :dataSource="pieChartData"
          >
          </pieChart>
        </div>
      </div>
      <div class="container-fluid" style="margin-top: 25px">
        <div class="row justify-content-center">
          <h3 class="display-10" style="color: black">
            Holdings in Detail
          </h3>
        </div>
        <div class="row justify-content-center">
          <div class="col-sm-12" id="header">
            <b-table :items="assets" class="mt-2" outlined head-variant="dark">
            </b-table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "./NavBar";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import { BTable } from "bootstrap-vue";
import Vue from "vue";
import VueFusionChartsComponent from "vue-fusioncharts/component";
import axios from "axios";
import {
  COMPUTE_WEIGHTS,
  COMPUTE_HISTORICAL_POS,
  COMPUTE_PNL,
} from "../config.js";

// import FusionCharts modules and resolve dependency
import FusionCharts from "fusioncharts";
import Charts from "fusioncharts/fusioncharts.charts";
import FusionTheme from "fusioncharts/themes/fusioncharts.theme.fusion";
import TimeSeries from "fusioncharts/fusioncharts.timeseries";

const pieChart = VueFusionChartsComponent(FusionCharts, Charts, FusionTheme);

const pnlChart = VueFusionChartsComponent(FusionCharts, Charts, FusionTheme);

const timeSeriesChart = VueFusionChartsComponent(
  FusionCharts,
  Charts,
  FusionTheme,
  TimeSeries
);

Vue.component("pieChart", pieChart);
Vue.component("pnlChart", pnlChart);
Vue.component("timeSeriesChart", timeSeriesChart);

export default {
  name: "Portfolio",
  data() {
    return {
      loading: false,
      api_key: "",
      api_secret: "",
      assets: {},
      computed_assets: {},
      componentKey: 0,
      pieChartData: {
        chart: {
          caption: "Current Portfolio Distribution",
          showValues: "1",
          showPercentInTooltip: "2",
          numberPrefix: "%",
          enableMultiSlicing: "1",
          theme: "fusion",
        },
        data: [],
      },
      timeSeriesSchema: [
        {
          name: "Time",
          type: "date",
        },
        {
          name: "Coin",
          type: "string",
        },
        {
          name: "Asset Value",
          type: "number",
        },
      ],
      timeSeriesData: {
        data: null,
        caption: {
          text: "Portfolio Net Asset Value",
        },
        subcaption: {
          text: "Over 4 Hourly Data",
        },
        series: "Coin",
        xAxis: { plot: "Time" },
        yAxis: [
          {
            plot: "Asset Value",
            title: "Asset Value",
            format: {
              prefix: "$",
            },
          },
        ],
      },
      pnlChartData: {
        chart: {
          caption: "Profit & Loss",
          subcaption: "Isolated by Individual Coins",
          numbersuffix: "$",
          showsum: "1",
          plottooltext: "$label $seriesName <b>$dataValue</b>",
          theme: "fusion",
        },
        categories: [
          {
            category: [],
          },
        ],
        dataset: [
          {
            seriesname: "Realised Profit",
            data: [],
          },
          {
            seriesname: "Unrealised Profit",
            data: [],
          },
        ],
      },
    };
  },
  components: {
    NavBar,
    Loading,
    BTable,
  },
  methods: {
    // Convert unix timestamp to date time format !!! Credit: @esd_mentino project
    timeConverter: function(UNIX_timestamp) {
      var a = new Date(UNIX_timestamp * 1000);
      Date.prototype.removeHours = function(hours) {
        this.setTime(this.getTime() - hours * 60 * 60 * 1000);
        return this;
      };
      a = a.removeHours(8);
      var months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ];
      var year = a.getFullYear();
      var month = months[a.getMonth()];
      var date = a.getDate();
      var hour = "0" + a.getHours();
      var min = "0" + a.getMinutes();
      // var sec = a.getSeconds();
      var time =
        date +
        " " +
        month +
        " " +
        year +
        " " +
        hour.substr(-2) +
        ":" +
        min.substr(-2);
      return time;
    },
    computeWeights() {
      axios.post(COMPUTE_WEIGHTS, { data: this.assets }).then((res) => {
        (this.pieChartData.data = res.data.plotting_data),
          (this.computed_assets = res.data.data);
      });
    },
    computePnl() {
      var json_payload = {
        API_KEY: this.api_key,
        API_SECRET: this.api_secret,
        order_history: this.order_history,
      };
      axios.post(COMPUTE_PNL, json_payload).then((res) => {
        this.pnlChartData.categories[0].category = res.data.data.categories;
        this.pnlChartData.dataset[0].data = res.data.data.real_pnl;
        this.pnlChartData.dataset[1].data = res.data.data.ureal_pnl;
        this.loading = false;
      });
    },
    computeHistoricalPosition() {
      axios
        .post(COMPUTE_HISTORICAL_POS, {
          data: this.order_history,
        })
        .then((res) => {
          // Endpoint returns time in unix form, need to convert back for Fusioncharts to parse
          var clean_data = [];
          res.data.data.forEach((item) =>
            clean_data.push([this.timeConverter(item[0]), item[1], item[2]])
          );
          const fusionTable = new FusionCharts.DataStore().createDataTable(
            clean_data,
            this.timeSeriesSchema
          );
          this.timeSeriesData.data = fusionTable;
        });
    },
  },
  mounted() {
    this.loading = true;
    this.api_secret = this.$store.state.api_details.secret;
    this.api_key = this.$store.state.api_details.key;
    this.assets = this.$store.state.assets;
    this.order_history = this.$store.state.order_history;
    this.computeWeights();
    this.computeHistoricalPosition();
    this.computePnl();
  },
};
</script>
