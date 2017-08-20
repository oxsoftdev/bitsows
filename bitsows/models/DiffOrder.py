from decimal import Decimal

from ._BaseModel import BaseModel


class DiffOrder(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book

        for (param, value) in data.items():
            if param == 'd':
                value = int(str(value)) / 1000.0
                setattr(self, 'timestamp', value)
            elif param == 'r':
                setattr(self, 'rate', Decimal(str(value)))
            elif param == 't':
                if value == 0:
                    setattr(self, 'type', 'bid')
                elif value == 1:
                    setattr(self, 'type', 'ask')
            elif param == 'a':
                setattr(self, 'amount', Decimal(str(value)))
            elif param == 'v':
                setattr(self, 'value', Decimal(str(value)))
            elif param == 'o':
                setattr(self, 'order_id', str(value))

    def __repr__(self):
        return "DiffOrder({DiffOrder})".format(
            DiffOrder=self._repr(
                'timestamp', 'book', 'type', 'rate', 'amount', 'value'
            )
        )

