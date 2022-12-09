import json
import os

import pika

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

AMQP_URL = os.environ.get('AMQP_URL')

class PikaClient:
    def __init__(self, queue):
        self.queue = queue
        parametrs = pika.URLParameters(AMQP_URL)
        self.connection = pika.BlockingConnection(parametrs)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def message_send(self, json_data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=json_data,
                                   properties=pika.BasicProperties(
                                       delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                   ))

    def connection_off(self):
        self.connection.close()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
            (r"/send", SendHandler),
        ]
        settings = dict(
            template_path="./src/templates/",
            static_path="./src/static/",
            xsrf_cookies=True,
            cookie_secret="262b44b297e695f78dcff3b56c8f43ac36235696"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("rootHandler.html")


class SendHandler(tornado.web.RequestHandler):
    def post(self):
        data = {'last_name': self.get_argument("last-name", default=None, strip=False),
                'first_name': self.get_argument("first-name", default=None, strip=False),
                'patronymic': self.get_argument("patronymic", default=None, strip=False),
                'phone': self.get_argument("phone", default=None, strip=False),
                'complaint_text': self.get_argument("appeal", default=None, strip=False)}
        json_data = json.dumps(data, ensure_ascii=False).encode("UTF-8")

        self.write(f"На сервер отправлено:{json_data.decode()}")

        # Message initialization
        message = PikaClient(queue="task_queue")
        message.message_send(json_data=json_data)
        message.connection_off()

        self.set_status(202)


def main():
    print('services running, press ctrl+c to stop')
    ioloop = tornado.ioloop.IOLoop.instance()
    app = Application()

    app.listen(80, "0.0.0.0")
    ioloop.start()


if __name__ == "__main__":
    main()
