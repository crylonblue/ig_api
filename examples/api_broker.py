from webservice import create_server_handler
from bot_handler import bot_handler
from datetime import datetime
from messaging_service import messaging_service
import socketserver
import json
import threading


class api_broker:

    def initiate_webserver(self):
        print("{time} - Starting webservice ...".format(time=datetime.now().strftime("%d.%m.%Y, %H:%M:%S")))
        self.serverHandler = create_server_handler(self)
        self.httpd = socketserver.TCPServer(("", 8083), self.serverHandler)
        self.httpd.serve_forever()

    def get_bot_handler_bots(self):
        response = []
        for bot in self.bot_handler.bots:
            response.append({
                "id": bot.bot_id,
                "username": bot.username,
                "proxy": bot.proxy,
                "status": bot.api.status,
                "messages_sent": bot.messages_sent,
                "shifts_skipped": bot.shifts_skipped,
                "device_id": bot.api.device_id
            })

        return json.dumps(response)

    def run_threaded(self, job_function, args):
        job_thread = threading.Thread(target=job_function, args=args)
        job_thread.start()

    def __init__(self):
        self.bot_handler = bot_handler(self, {
            "start_with_messaging_service": True,
            "start_with_warmup_service": False
        })

        self.messaging_service = messaging_service(self.bot_handler)
        self.run_threaded(self.initiate_webserver, ())
        self.run_threaded(self.bot_handler.initiate_bot_handler, ())


api_broker()



