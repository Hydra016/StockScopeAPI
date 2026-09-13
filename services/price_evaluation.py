from controllers.stocks import get_quote
from models.alert import AlertModel
from sqlalchemy.orm import Session


class PriceEvaluationService:
    def __init__(self, alert: AlertModel):
        self.alert = alert

    async def evaluate(self, db: Session):
        if not self.alert.is_active:
            return False

        stock_data = await get_quote(self.alert.symbol, db)
        current_price = stock_data.data.current_price
        triggered = False

        if self.alert.condition == "ABOVE":
            triggered = current_price > self.alert.target_price


        if self.alert.condition == "BELOW":
            triggered = current_price < self.alert.target_price

        return triggered