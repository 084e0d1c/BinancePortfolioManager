class CoinProfitLoss:

    def __init__(self,name):
        self.name = name
        self.cost_basis = 0
        self.realised_profit_loss = 0
        self.quantity = 0

    def buy(self,executedQty: float, price: float):
        self.quantity += executedQty
        self.cost_basis += executedQty * price

    def sell(self,executedQty: float, price: float):
        avg_purchase_price = self.cost_basis / self.quantity
        profit_loss = price - avg_purchase_price
        self.realised_profit_loss += profit_loss * executedQty
        self.quantity -= executedQty
        self.cost_basis = self.quantity * avg_purchase_price

    def get_realised_pnl(self):
        return self.realised_profit_loss

    def get_unrealised_pnl(self,current_price):
        current_mkt_value = self.quantity * current_price
        return current_mkt_value - self.cost_basis

    def total_pnl(self,current_price):
        return self.get_realised_pnl() + self.get_unrealised_pnl(current_price)