import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import settings
import time
import threading
import logging
import signal
import json


class SendUpdates():
    def __init__(self, interval):
        print("SendUpdates.__init__")
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        
    def run(self):
        while True:
            print("SendUpdates.run(). connections.len = %d" % len(WSHandler.connections))
            for conn in WSHandler.connections:
                try:
                    conn.write_message("JSON Data here!")
                except Exception as e:
                    print("Exception writing to websocket: %s" % e)
            time.sleep(self.interval)


class WSHandler(tornado.websocket.WebSocketHandler):
    connections = []

    # def __init__(self, application, request, **kwargs):
    #     super(WSHandler, self).__init__(application, request, **kwargs)
    #     print("WSHandler")

    # def __del__(self):
    #     print("WSHandler.__del__")

    def open(self):
        print('new connection')
        if(self.request.headers['Authorization'] != settings.AUTH_KEY):
            self.close()
        else:
            WSHandler.connections.append(self)
      
    def on_message(self, message):
        try:
            print('message received:  %s' % message)
            # Reverse Message and send it back
            print('sending back message: %s' % message[::-1])
            self.write_message(message[::-1])
        except Exception:
            pass
 
    def on_close(self):
        print('connection closed')
        if self in WSHandler.connections:
            WSHandler.connections.remove(self)
        
 
    def check_origin(self, origin):
        return True


class HTTPHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(HTTPHandler, self).__init__(application, request, **kwargs)
        print("HTTPHandler.__init__")

    def __del__(self):
        print("HTTPHandler.__del__")

    def get(self):
        data = {'key': 'value'}
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data))


class Server():
    # Adapted from code found at https://gist.github.com/mywaiting/4643396
    def sig_handler(self, sig, frame):
        logging.warning("Caught signal: %s", sig)
        tornado.ioloop.IOLoop.instance().add_callback(self.shutdown)

    def __init__(self, port=8888):
        application = tornado.web.Application([
            (r"/", HTTPHandler),
            (r'/ws', WSHandler),
        ])
        send_updates = SendUpdates(settings.SEND_UPDATE_TICK)
        server = tornado.httpserver.HTTPServer(application)
        server.listen(port)

        self.server = server
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        tornado.ioloop.IOLoop.instance().start()
        logging.info("Exit...")

    def shutdown(self):
        logging.info('Stopping HTTP Server.')
        self.server.stop()

        logging.info('Will shutdown in %s seconds...', settings.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)

        io_loop = tornado.ioloop.IOLoop.instance()

        deadline = time.time() + settings.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def stop_loop():
            now = time.time()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()
                logging.info('Shutdown')
        stop_loop()


# def server(port=8888):
#     application = tornado.web.Application([
#         (r"/", HTTPHandler),
#         (r'/ws', WSHandler),
#     ])
#     send_updates = SendUpdates(5)
#     application.listen(port)
#     tornado.ioloop.IOLoop.current().start()

