from decimal import Decimal
from datetime import datetime
from time import time

from ._BaseModel import BaseModel
from .OrderUpdate import OrderUpdate
from .TradeUpdate import TradeUpdate


class StreamUpdate(BaseModel):

    def __init__(self, data):
        self._timestamp = time()
        self._datetime = datetime.fromtimestamp(self._timestamp)
        self.book = data['book']
        self.type = data['type']
        self.sequence_no = None
        self.payload = []

        if 'sequence' in data:
            self.sequence_no = int(data['sequence'])

        if 'payload' in data:
            if self.type == 'diff-orders':
                self.payload = self._build_diff_order_updates(
                    data['payload'])
            elif self.type == 'trades':
                self.payload = self._build_trade_updates(data['payload'])
            elif self.type == 'orders':
                self.payload = self._build_order_updates(data['payload'])

    def _build_object_updates(self, payload, type):
        l = []
        for o in payload:
            _o = type(self._timestamp, self.book, **o)
            l.append(_o)
        return l

    def _build_trade_updates(self, payload):
        return self._build_object_updates(payload, TradeUpdate)

    def _build_diff_order_updates(self, payload):
        return self._build_object_updates(payload, OrderUpdate)

    def _build_order_updates(self, payload):
        asks = self._build_object_updates(payload['asks'], OrderUpdate)
        bids = self._build_object_updates(payload['bids'], OrderUpdate)
        return asks + bids

    def __repr__(self):
        return "StreamUpdate({StreamUpdate})".format(
            StreamUpdate=self._repr('book', 'type')
        )

