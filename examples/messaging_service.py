import csv


class messaging_service:

    def check_if_in_queue(self, user_id):
        for bot in self.bot_handler.bots:
            for message in bot.messages:
                if message[0] == user_id:
                    return True
        return False

    def skipped(self, user_id):
        with open(self.skipped_file) as f:
            if user_id in f.read():
                return True
        return False

    def messaged(self, user_id):
        with open(self.messaged_file) as f:
            if user_id in f.read():
                return True
        return False

    def mark_skipped(self, user_id):
        skipped = open(self.skipped_file, "a+")
        with skipped:
            skipped.write(user_id + "\n")

    def mark_messaged(self, user_id):
        messaged_file_handler = open(self.messaged_file, "a+")
        with messaged_file_handler:
            messaged_file_handler.write(user_id + "\n")

    def file_len(self, file_path):
        with open(file_path) as f:
            i = 0
            for i, l in enumerate(f):
                pass
            return i + 1

    def get_messages(self, amount):
        messages = []
        database_handle = open(self.message_database, "r")

        with database_handle:
            reader = csv.reader(database_handle, delimiter=",")
            line_count = 0
            for line in reader:

                if len(messages) >= amount:
                    continue

                if line_count != 0:
                    user_id = line[0]
                    username = line[1]
                    message = line[2]

                    if not self.check_if_in_queue(user_id) and not self.messaged(user_id) and not self.skipped(user_id):
                        messages.append([user_id, username, message])

                line_count += 1

        return messages

    def __init__(self, bot_handler):
        self.status = "healthy"
        self.skipped_file = "messaging_service/skipped.txt"
        self.messaged_file = "messaging_service/messaged.txt"
        self.message_database = "messaging_service/messages_db.csv"
        self.bot_handler = bot_handler
