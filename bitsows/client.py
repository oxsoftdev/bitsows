import json
import logging
import tornado.gen
import tornado.websocket
from dppy.behavioral import pubsub

from .models import StreamUpdate


logger = logging.getLogger('bitsows')


class BitsoClient(pubsub.AbsPublisher):

    def __init__(self, ):
        self._ws_client = None
        self._ws_url = 'wss://ws.bitso.com'
        self._channels = ['diff-orders', 'trades', 'orders']
        self._books = ['btc_mxn', 'eth_mxn', 'xrp_btc', 'xrp_mxn', 'eth_btc']

    @tornado.gen.coroutine
    def connect(self):
        logger.info("connecting")
        try:
            websocket_connect = tornado.websocket.websocket_connect
            self._ws_client = yield websocket_connect(self._ws_url)
            self.subscribe()
        except:
            logger.exception("failed to connect")
        else:
            logger.info("connected")
            self.listen()

    @tornado.gen.coroutine
    def listen(self):
        while True:
            try:
                msg = yield self._ws_client.read_message()
                if msg is None:
                    logger.info("connection closed")
                    self._ws_client = None
                    break
                else:
                    _json = json.loads(msg)
                    if (isinstance(_json, dict) and 'payload' in _json):
                        self.notify(StreamUpdate(_json))
                    else:
                        logger.info(msg)
            except:
                logger.exception("failed on listen")
                raise

    def subscribe(self):
        for channel in self._channels:
            for book in self._books:
                logger.info("subscribing(channel=%s,book=%s)" %
                            (channel, book))
                self._ws_client.write_message(json.dumps({
                    'action': 'subscribe',
                    'book': book,
                    'type': channel
                }))

