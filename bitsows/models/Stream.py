from decimal import Decimal

from ._BaseModel import BaseModel
from .DiffOrder import DiffOrder
from .Order import Order
from .Trade import Trade


class Stream(BaseModel):

    def __init__(self, timestamp, datetime, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = data['book']
        self.type = data['type']
        self.sequence_no = None
        self.payload = []

        if 'sequence' in data:
            self.sequence_no = int(str(data['sequence']))

        if 'payload' in data:
            if self.type == 'diff-orders':
                self.payload = self._build_diff_order_updates(
                    data['payload'])
            elif self.type == 'orders':
                self.payload = self._build_order_updates(data['payload'])
            elif self.type == 'trades':
                self.payload = self._build_trade_updates(data['payload'])

    def _build_object(self, payload, type):
        l = []
        for o in payload:
            _o = type(self._timestamp, self._datetime, self.book, o)
            l.append(_o)
        return l

    def _build_diff_order_updates(self, payload):
        return self._build_object(payload, DiffOrder)

    def _build_order_updates(self, payload):
        asks = self._build_object(payload['asks'], Order)
        bids = self._build_object(payload['bids'], Order)
        return asks + bids

    def _build_trade_updates(self, payload):
        return self._build_object(payload, Trade)

    def __repr__(self):
        return "Stream({Stream})".format(
            Stream=self._repr('book', 'type')
        )

