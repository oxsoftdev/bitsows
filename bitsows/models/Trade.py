from decimal import Decimal
from datetime import datetime

from ._BaseModel import BaseModel


class TradeUpdate(BaseModel):

    def __init__(self, _timestamp, book, **kwargs):
        self._timestamp = _timestamp
        self._datetime = datetime.fromtimestamp(self._timestamp)
        self.book = book
        for (param, value) in kwargs.items():
            if param == 'i':
                setattr(self, 'tid', int(value))
            elif param == 'a':
                setattr(self, 'amount', Decimal(str(value)))
            elif param == 'r':
                setattr(self, 'rate', Decimal(str(value)))
            elif param == 'v':
                setattr(self, 'value', Decimal(str(value)))
            elif param == 't':
                if value == 0:
                    setattr(self, 'type', 'buy')
                elif value == 1:
                    setattr(self, 'type', 'sell')
            elif param == 'mo' and value:
                setattr(self, 'maker_order_id', value)
            elif param == 'to' and value:
                setattr(self, 'taker_order_id', value)

    def __repr__(self):
        return "TradeUpdate({TradeUpdate})".format(
            TradeUpdate=self._repr('book','tid','rate','amount','value')
        )
