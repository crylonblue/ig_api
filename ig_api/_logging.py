import os


def log(self, log_text):
    if not os.path.isfile(self.log_file):
        with open(self.log_file, "w"):
            pass

    with open(self.log_file, "a") as log_file:
        log_file.write(str(log_text) + "\n")
