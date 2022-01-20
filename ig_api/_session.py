from . import constants
import uuid
import hashlib
import os
import random
import json

def generate_new_session_ids(self):
        self.pigeon_session_id = self.generate_random_uuid()
        self.session_id = self.generate_random_uuid()

def generate_new_uuids(self):
    self.log("[INFO] generating fresh uuids ...")
    self.device_id = self.generate_random_uuid()
    self.device_token = str(self.get_seed("device_token")) + str(self.get_seed("device_token_second_part"))
    self.ios_voip_device_token = str(self.get_seed("ios_voip_device_token")) + str(self.get_seed("ios_voip_device_token"))
    self.generate_new_session_ids()

def generate_random_uuid(self, without_hyphen=False):
    return str(uuid.uuid4()).replace("-", "") if without_hyphen else str(uuid.uuid4()).upper()

def get_seed(self, *args):
    m = hashlib.md5()
    m.update(b"".join([arg.encode("utf-8") for arg in args]))
    return m.hexdigest()

def restore_from_session_file(self):
    if os.path.isfile(self.session_file):
        with open(self.session_file, "r") as session_file:
            session_json = json.load(session_file)
            self.authorization = session_json["authorization"]
            self.password = session_json["password"]
            self.u_rur = session_json["ig-u-rur"]
            self.ds_user_id = session_json["ig-u-ds-user-id"]
            self.mid = session_json["x-mid"]
            self.device_id = session_json["device_id"]
            self.username = session_json["username"]
            self.is_dark_mode = session_json["is_dark_mode"]
            self.proxy = session_json["proxy"]
            self.session_id = session_json["session_id"]
            self.pigeon_session_id = session_json["pigeon_session_id"]
            self.device_token = session_json["device_token"]
            self.ios_voip_device_token = session_json["ios_voip_device_token"]
            self.log("[INFO] restore {} session, {} pigeon session".format(self.session_id, self.pigeon_session_id))
            self.session_start = session_json["session_start"]
            if "x-ig-www-claim" in session_json:
                self.claim = session_json["x-ig-www-claim"]
            self.setup_logged_in_headers()
        return True
    else:
        return False


def save_session_ids(self):
    if os.path.isfile(self.session_file):
        save_file = None
        with open(self.session_file, "r") as json_file:
            save_file = json.loads(json_file.read())

        save_file["session_id"] = self.session_id
        save_file["pigeon_session_id"] = self.pigeon_session_id

        with open(self.session_file, "w") as json_file:
            json.dump(save_file, json_file)


def save_login_session(self, login_headers, claim=None):
    self.log("[INFO][{}] setup sso headers".format(self.username))
    self.authorization = login_headers["ig-set-authorization"]
    self.u_rur = login_headers["ig-set-ig-u-rur"]
    self.ds_user_id = login_headers["ig-set-ig-u-ds-user-id"]
    self.headers["authorization"] = self.authorization
    self.headers["ig-u-rur"] = self.u_rur
    self.headers["ig-u-ds-user-id"] = self.ds_user_id

    self.session.headers.update(self.headers)
    self.is_dark_mode = random.randint(0, 1)
    self.is_charging = random.randint(0, 1)

    save_file = {
        "authorization": self.authorization,
        "ig-u-rur": self.u_rur,
        "ig-u-ds-user-id": self.ds_user_id,
        "x-mid": self.mid,
        "device_id": self.device_id,
        "device_token": self.device_token,
        "ios_voip_device_token": self.ios_voip_device_token,
        "username": self.username,
        "password": self.password,
        "is_dark_mode": self.is_dark_mode,
        "proxy": self.proxy,
        "session_id": self.session_id,
        "pigeon_session_id": self.pigeon_session_id,
        "session_start": self.session_start
    }

    with open(self.session_file, "w") as json_file:
        json.dump(save_file, json_file)


def save_claim(self, claim):
    if os.path.isfile(self.session_file):
        save_file = None
        with open(self.session_file, "r") as json_file:
            save_file = json.loads(json_file.read())

        save_file["x-ig-www-claim"] = claim

        with open(self.session_file, "w") as json_file:
            json.dump(save_file, json_file)


def delete_session(self):
    self.log("[API][{}] session broken, deleting session".format(self.username))
    if os.path.isfile(self.session_file):
        os.rename(self.session_file, "sessions/removed/" + self.username + "_session.json")
