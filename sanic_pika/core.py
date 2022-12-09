# -*- coding: utf-8 -*-


import aio_pika
from apika import Apika

from sanic import Sanic
from sanic.log import logger


class SanicPika:

    conn: aio_pika.RobustConnection
    app: Sanic
    url: str
    config_name: str

    def __init__(self,
                 app: Sanic,
                 config_name: str = "RABBIT_MQ",
                 attr_name: str = "RABBIT_MQ",
                 url: str = "",
                 *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.app: Sanic = app
        self.url: str = url
        self.conn: aio_pika.RobustConnection
        self.config_name: str = config_name
        self.attr_name: str = attr_name

        if app:
            self.init_app()

    def init_app(self):
        app = self.app

        @app.listener('before_server_start')
        async def aio_pika_configure(_app: Sanic, _loop):
            if self.url:
                _url = self.url
            else:
                _url = _app.config.get(self.config_name)
            if not _url:
                raise ValueError("You must specify a url or set the {} Sanic config variable".format(self.config_name))
            logger.info("[sanic-pika] connecting..")
            _mq = Apika(_url, *self.args, **self.kwargs)
            await _mq.init_app()
            setattr(_app.ctx, self.attr_name.lower(), _mq)
            self.conn = _mq

        @app.listener('after_server_stop')
        async def close_pika(_app, _loop):
            logger.info("[sanic-pika] closing..")
            await self.conn.close()
