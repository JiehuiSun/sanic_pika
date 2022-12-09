# -*- coding: utf-8 -*-


from sanic_pika import SanicPika
from sanic import Sanic
from sanic.log import logger
from typing import Any
from sanic.response import json as send_json


app = Sanic('app')
app.config["RABBIT_MQ"] = "amqp://guest:guest@127.0.0.1/"

SanicPika(app)

"""
# NOTE: Parameters can be configured arbitrarily

# For example:
SanicPika(app, attr_name="amq", queue_name="queue", exchange="exchange", routing_key="test")

await app.ctx.amq.get()

"""


@app.listener('before_server_start')
async def before_server_start(app: Sanic, loop):
    logger.info(">> before_server_start")
    app.add_task(__task_test_pika, name="_test")


@app.listener('before_server_stop')
async def before_server_stop(app: Sanic, loop):
    await app.ctx.rabbit_mq.close()


async def __callback(data: Any, app: Sanic):
    logger.info("Msg is %s" % data)


async def __task_test_pika(app: Sanic):
    while True:
        try:
            await app.ctx.rabbit_mq.get(__callback, (app,))
        except Exception as e:
            logger.error(e)


@app.route('/test_push', methods=['POST'])
async def on_push(req):
    await req.app.ctx.rabbit_mq.push(req.json or {})
    return send_json({})


if __name__ == "__main__":
    app.run(dev=True, debug=True, host="127.0.0.1", port=8888)
