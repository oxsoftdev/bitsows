from decimal import Decimal
from datetime import datetime

from ._BaseModel import BaseModel


class OrderUpdate(BaseModel):

    def __init__(self, _timestamp, book, **kwargs):
        self._timestamp = _timestamp
        self._datetime = datetime.fromtimestamp(self._timestamp)
        self.book = book
        for (param, value) in kwargs.items():
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

    def __str__(self):
        return "OrderUpdate({OrderUpdate})".format(
            OrderUpdate=self._repr(
                'timestamp', 'book', 'type', 'rate', 'amount', 'value'
            )
        )

