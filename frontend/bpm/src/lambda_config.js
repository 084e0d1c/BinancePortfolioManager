// Lambda Endpoints
const APIGATEWAY_HOST =
  "https://l16died99a.execute-api.ap-southeast-1.amazonaws.com/dev";
export const COMPUTE_WEIGHTS = APIGATEWAY_HOST + "/compute_weights";
export const COMPUTE_HISTORICAL_POS = APIGATEWAY_HOST + "/compute_position";
export const COMPUTE_PNL = APIGATEWAY_HOST + "/compute_pnl";
export const GET_ALL_TRADES = APIGATEWAY_HOST + "/get_all_trades";
export const GET_TICKERS = APIGATEWAY_HOST + "/get_valid_tickers";
