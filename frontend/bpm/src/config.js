// DEV Switch
export const DEV = false;
export let COMPUTE_WEIGHTS;
export let COMPUTE_HISTORICAL_POS;
export let COMPUTE_PNL;
export let GET_ALL_TRADES;
export let GET_TICKERS;
export let TRADED_PAIRS;
export let CRUD_TRADED_PAIRS;

if (DEV) {
  const HOSTNAME = "http://localhost:";
  COMPUTE_WEIGHTS = HOSTNAME + "5001/compute_weights";
  COMPUTE_HISTORICAL_POS = HOSTNAME + "5003/compute_historical_positions";
  COMPUTE_PNL = HOSTNAME + "5004/compute_pnl";
  GET_TICKERS = HOSTNAME + "5005/get_tickers";
  TRADED_PAIRS = [
    "ETHUSDT",
    "ALGOUSDT",
    "BTCUSDT",
    "ZILUSDT",
    "BNBUSDT",
    "EGLDUSDT",
    "DOTUSDT",
    "NEARUSDT",
    "ATOMUSDT",
    "DOTBTC",
  ];
} else {
  const APIGATEWAY_HOST =
    "https://l16died99a.execute-api.ap-southeast-1.amazonaws.com/dev";
  COMPUTE_WEIGHTS = APIGATEWAY_HOST + "/compute_weights";
  COMPUTE_HISTORICAL_POS = APIGATEWAY_HOST + "/compute_position";
  COMPUTE_PNL = APIGATEWAY_HOST + "/compute_pnl";
  GET_ALL_TRADES = APIGATEWAY_HOST + "/get_all_trades";
  GET_TICKERS = APIGATEWAY_HOST + "/get_valid_tickers";
  CRUD_TRADED_PAIRS =
    "https://4vjabqb5tj.execute-api.ap-southeast-1.amazonaws.com/dev/userpairs";
}
