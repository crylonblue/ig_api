from ig_api import ig_api
import uuid
import time
import json
import threading
import random
import schedule
from simulator import simulator

class bot_wrapper:

    def log(self, log_text):
        self.api.log(log_text)

    def messaging_shift(self):
        self.log("[BOT][{}] performing messaging shift".format(self.username))
        self.api.startup_app()
        time.sleep(random.randint(3, 30))

        self.messages = self.messaging_service.get_messages(amount=random.randint(self.messages_per_shift_min, self.messages_per_shift_max))
        self.send_messages()

    def perform_random_actions(self):

        if random.random() < 0.1:
            self.simulator.like_random_from_timeline()

        if random.random() < 0.1:
            self.api.pull_to_refresh()
            time.sleep(random.randint(5, 15))

        if random.random() < 0.03:
            self.simulator.simulate_viewing_reels()
            time.sleep(random.randint(5, 15))

        if random.random() < 0.1:
            self.simulator.simulate_scrolling()
            time.sleep(random.randint(5, 15))

        if random.random() < 0.05:
            self.simulator.simulate_random_search()
            time.sleep(random.randint(5, 15))

    def send_messages(self):
        try:
            for message in self.messages:
                self.perform_random_actions()
                if self.api.logged_in and self.api.status != "feedback_required":
                    user_id = message[0]
                    username = message[1]
                    text = message[2]

                    if self.send_message(user_id, username, text):
                        self.messaging_service.mark_messaged(user_id)
                        self.messages_sent += 1
                    else:
                        self.messaging_service.mark_skipped(user_id)

                time.sleep(random.randint(50, 180))

            if self.api.status == "feedback_required":
                wait_shifts = 3
                if self.shifts_skipped >= wait_shifts:
                    self.api.status = "valid"
                    self.shifts_skipped = 0

                self.shifts_skipped += 1
                self.warm_up_shift()


        except Exception as e:
            self.log(e)
            # pass

        self.messages = []

    def send_message(self, user_id, username, text):
        if self.simulator.check_simulate_search_user(user_id, username):
            self.api.get_search_dynamic_sections()
            self.simulator.simulate_show_user(user_id)
            return self.api.send_text_message_to_userid(user_id, text)
        return False

    def send_message_to_username(self, username, text):
        return self.api.send_text_message_to_username(username, text)

    def get_random_time_string(self, from_hour, to_hour):
        return "{:02d}:{:02d}".format(random.randint(from_hour, (to_hour - 1)), random.randint(0, 59))

    def schedule_new_shifts(self):
        shift1 = self.get_random_time_string(7, 9)
        shift2 = self.get_random_time_string(13, 16)
        shift3 = self.get_random_time_string(19, 21)
        self.log("[BOT] Scheduled shifts: {}, {}, {}".format(shift1, shift2, shift3))
        schedule.every().day.at(shift1).do(
            lambda: self.run_threaded_once(self.messaging_shift, ()))
        schedule.every().day.at(shift2).do(
            lambda: self.run_threaded_once(self.messaging_shift, ()))
        schedule.every().day.at(shift3).do(
            lambda: self.run_threaded_once(self.messaging_shift, ()))

    def setup_messaging_service(self, messaging_service):
        self.log("[BOT][{}] setup messaging service".format(self.username))
        self.messaging_service = messaging_service
        schedule.every().day.at("04:00").do(
            lambda: self.run_threaded(self.schedule_new_shifts, ()))

    def setup_warmup_service(self):
        self.log("[BOT][{}] setup warm up shifts".format(self.username))
        schedule.every().day.at(self.get_random_time_string(18, 21)).do(
            lambda: self.run_threaded(self.warm_up_shift, ()))

    def warm_up_shift(self):
        self.log("[BOT][{}] perform warm up shift".format(self.username))
        time.sleep(random.randint(15, 45))
        warm_up_functions = [self.simulator.simulate_viewing_reels, self.simulator.like_random_from_timeline, self.simulator.simulate_random_search, self.simulator.simulate_scrolling, self.simulator.simulate_scrolling, self.api.pull_to_refresh]
        random.shuffle(warm_up_functions)

        for function in warm_up_functions:
            if random.random() > 0.5:
                function()
                time.sleep(random.randint(15, 45))

    def run_threaded(self, job_function, args):
        job_thread = threading.Thread(target=job_function, args=args)
        job_thread.start()

    def run_threaded_once(self, job_function, args):
        job_thread = threading.Thread(target=job_function, args=args)
        job_thread.start()
        return schedule.CancelJob

    def donwload_inbox(self, amount):
        self.log("[BOT][{}] downloading inbox".format(self.username))
        threads = []
        oldest_cursor = None

        if self.api.inbox:
            for thread in self.api.inbox["threads"]:
                threads.append(thread)

            if "oldest_cursor" in self.api.inbox:
                oldest_cursor = self.api.inbox["oldest_cursor"]
        else:
            self.api.inbox = self.api.get_inbox(reason="pull_to_refresh")
            for thread in self.api.inbox["threads"]:
                threads.append(thread)
            if "oldest_cursor" in self.api.inbox:
                oldest_cursor = self.api.inbox["oldest_cursor"]

        while oldest_cursor is not None and len(threads) > amount:
            try:
                next_page = self.api.get_inbox(reason="pagination", cursor=oldest_cursor)

                if next_page:
                    for thread in next_page["threads"]:
                        threads.append(thread)
                    if "oldest_cursor" in next_page:
                        oldest_cursor = next_page["oldest_cursor"]
                    else:
                        oldest_cursor = None
            except:
                oldest_cursor = None
            time.sleep(random.randint(20, 40))

        self.save_threads(threads)

    def save_threads(self, threads):
        save_path = "inbox/" + self.username + "_threads.json"

        inbox = {
            "user": self.username,
            "updated": time.time(),
            "inbox": threads
        }

        with open(save_path, "w+") as file:
            file.write(json.dumps(inbox))

    def __init__(self, bot_handler, username, password, proxy, options):
        self.bot_id = str(uuid.uuid4())
        self.messaging_service = None
        self.username = username
        self.password = password
        self.proxy = proxy
        self.session_file = "sessions/" + username + "_session.json"
        self.log_file = "sessions/" + username + "_log.txt"
        self.messages_per_shift_min = 5
        self.messages_per_shift_max = 12
        # to help skipping shifts
        self.shifts_skipped = 0
        # to store messages from messaging service
        self.messages = []
        self.messages_sent = 0
        self.api = ig_api(self.username, self.password, self.proxy)
        self.bot_handler = bot_handler
        self.simulator = simulator(self.api)

        if self.bot_handler and options["start_with_messaging_service"]:
            self.setup_messaging_service(self.bot_handler.api_broker.messaging_service)

        if options["start_with_warmup_service"]:
            self.setup_warmup_service()

        self.api.startup_app()
