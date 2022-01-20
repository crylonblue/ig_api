from glob import glob
import time
import json
import threading
import schedule
from bot_wrapper import bot_wrapper
from datetime import datetime

class bot_handler:

    def run_schedule_service(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def session_active(self, session_file):
        for bot in self.bots:
            if bot.session_file == session_file:
                return True
        return False

    def refresh_sessions(self):
        print("[BOTHANDLER][{}] refresh sessions".format(datetime.now().strftime("%d.%m.%Y, %H:%M:%S")))
        remove_array = []
        for bot in self.bots:
            if not bot.api.logged_in:
                try:
                    bot.api.delete_session()
                except Exception as e:
                    print("[BOTHANDLER] error occured, while deleting")
                    print(e)
                remove_array.append(bot)

        for bot in remove_array:
            self.bots.remove(bot)

        session_files = glob("sessions/*.json")

        for session_file in session_files:
            if not self.session_active(session_file):
                self.run_threaded(self.start_session_from_session_file, (session_file,))
                # we do a little time sleep to prevent same proxy detection
                time.sleep(5)

    def start_session_from_session_file(self, session_file_path):
        print("[BOTHANDLER] added session from " + session_file_path)
        with open(session_file_path, "r") as session_file:
            session_json = json.loads(session_file.read())
            username = session_json["username"]
            password = session_json["password"]
            proxy = session_json["proxy"]
            self.bots.append(bot_wrapper(self, username, password, proxy, self.options))

    def get(self, id):
        for bot in self.bots:
            if bot.bot_id == id:
                return bot
        return None


    def run_threaded(self, job_function, args):
        job_thread = threading.Thread(target=job_function, args=args)
        job_thread.start()

    def initiate_bot_handler(self):
        self.run_threaded(self.refresh_sessions, ())
        schedule.every().hour.do(lambda: self.run_threaded(self.refresh_sessions, ()))
        self.run_threaded(self.run_schedule_service, ())

    def __init__(self, api_broker, options):
        self.bots = []
        self.options = options
        self.api_broker = api_broker


