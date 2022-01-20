from http.server import BaseHTTPRequestHandler
import json
import re


def create_server_handler(broker):
    class Server(BaseHTTPRequestHandler):
        def _set_headers(self):
            try:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
            except:
                pass

        def do_HEAD(self):
            try:
                self._set_headers()
            except:
                pass

        def do_GET(self):
            try:
                self._set_headers()
                if re.search("/bot/(.*)/timeline", self.path):
                    bot_id = self.path.split("/")[-2]
                    bot = self.broker.bot_handler.get(bot_id)
                    if bot:
                        timeline = bot.api.timeline
                        self.wfile.write(json.dumps(timeline).encode())

                if re.search("/bot/(.*)/inbox", self.path):
                    bot_id = self.path.split("/")[-2]
                    bot = self.broker.bot_handler.get(bot_id)
                    if bot:
                        inbox = bot.api.inbox
                        self.wfile.write(json.dumps(inbox).encode())

                if re.search("/bot/(.*)/reels", self.path):
                    bot_id = self.path.split("/")[-2]
                    bot = self.broker.bot_handler.get(bot_id)
                    if bot:
                        reels = bot.api.reels
                        self.wfile.write(json.dumps(reels).encode())

                if re.search("/bot/(.*)/reels_media", self.path):
                    bot_id = self.path.split("/")[-2]
                    bot = self.broker.bot_handler.get(bot_id)
                    if bot:
                        reels_media = bot.api.reels_media
                        self.wfile.write(json.dumps(reels_media).encode())

                if re.search("/bot/(.*)/explore", self.path):
                    bot_id = self.path.split("/")[-2]
                    bot = self.broker.bot_handler.get(bot_id)
                    if bot:
                        explore = bot.api.explore
                        self.wfile.write(json.dumps(explore).encode())

                elif re.search("/bots", self.path):
                    self.wfile.write(self.broker.get_bot_handler_bots().encode())
            except:
                pass


        def __init__(self, *args, **kwargs):
            self.broker = broker
            super(Server, self).__init__(*args, **kwargs)

        def log_message(self, format, *args):
            pass

    return Server



