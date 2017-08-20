from decimal import Decimal

from ._BaseModel import BaseModel


class Order(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book

        for (param, value) in data.items():
            if param == 'r':
                setattr(self, 'rate', Decimal(str(value)))
            elif param == 'a':
                setattr(self, 'amount', Decimal(str(value)))
            elif param == 'v':
                setattr(self, 'value', Decimal(str(value)))
            elif param == 't':
                if value == 0:
                    setattr(self, 'type', 'bid')
                elif value == 1:
                    setattr(self, 'type', 'ask')
            elif param == 'd':
                value = int(value) / 1000.0
                setattr(self, 'timestamp', value)
                setattr(self, 'datetime', datetime.fromtimestamp(value))

    def __repr__(self):
        return "Order({Order})".format(
            Order=self._repr(
                'timestamp', 'book', 'type', 'rate', 'amount', 'value'
            )
        )

