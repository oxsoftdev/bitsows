from decimal import Decimal

from ._BaseModel import BaseModel


class Trade(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book

        for (param, value) in data.items():
            if param == 'i':
                setattr(self, 'tid', int(str(value)))
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
        return "Trade({Trade})".format(
            Trade=self._repr('book','tid','rate','amount','value')
        )

