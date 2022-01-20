from . import constants
import hashlib
import time
import base64
import random
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_v1_5
import datetime
import struct
import json
from Cryptodome.PublicKey import RSA


def setup_logged_in_headers(self):
    self.headers["authorization"] = self.authorization
    self.headers["ig-u-rur"] = self.u_rur
    self.headers["ig-u-ds-user-id"] = self.ds_user_id
    self.headers["x-ig-device-id"] = self.device_id
    self.headers["x-ig-family-device-id"] = self.device_id
    self.headers["x-mid"] = str(self.mid)
    self.headers["ig-intended-user-id"] = self.ds_user_id
    self.headers["x-ig-www-claim"] = str(self.claim)
    self.headers["x-pigeon-session-id"] = self.pigeon_session_id
    self.session.headers.update(self.headers)


def setup_prelogin_headers(self):
    self.headers["x-mid"] = str(self.mid)
    self.headers["ds_user_id"] = self.ds_user_id
    self.headers["ig-intended-user-id"] = "0"
    self.session.headers.update(self.headers)


def login(self, username, password):
    try:
        self.username = username
        self.password = password

        dict_data = {
            "phone_id": self.device_id,
            "reg_login": "0",
            "device_id": self.device_id,
            "has_seen_aart_on": "0",
            "att_permission_status": "2",
            "username": self.username,
            "login_attempt_count": "0",
            "enc_password": self.encrypt_password(self.password)
        }

        signature = self.sign_json(dict_data)

        response = self.post("accounts/login/", data=signature, headers=self.session.headers)
        
        if response.status_code == 200:
            logged_in_json = self.get_json(response)

            if logged_in_json["status"] == "ok":
                self.save_login_session(response.headers)
                return True
            else:
                self.log(logged_in_json)
                return False

        elif response.status_code == 400:
            self.log(response.content)
            try:
                response_json = self.get_json(response)

                if response_json["message"] == "challenge_required":
                    time.sleep(2)
                    challenge_path = response_json["challenge"]["api_path"][1:]
                    challenge_options = self.get(challenge_path)
                    challenge_options_json = self.get_json(challenge_options)
                    time.sleep(random.randint(2, 4))

                    if "step_name" in challenge_options_json:
                        if challenge_options_json["step_name"] == "select_verify_method":
                            if "email" in challenge_options_json["step_data"]:
                                choicereq = self.post(challenge_path, data=self.sign_json({"choice": "1", "guid": self.device_id, "device_id": self.device_id}))
                                self.log("[CHALLENGE] Email Verification send to: {}".format(challenge_options_json["step_data"]["email"]))
                                security_code = input("[CHALLENGE] Insert Code:")
                                time.sleep(random.randint(2, 4))
                                solving_request = self.post(challenge_path, data=self.sign_json({"security_code": security_code, "guid": self.device_id, "device_id": self.device_id}))
                                self.save_login_session(solving_request.headers)
                                return True
                            else:
                                self.log("[CHALLENGE] Unable to solve challenge")
                return False

            except:
                self.log("[ERROR] Trying solving challenge")
                return False

        else:
            self.log("[WARNING] Login failed: " + self.get_json(response)["message"])
            return False
    except:
        self.log("[ERROR] While trying to login")
        return False

def relogin(self):
    if self.login(self.username, self.password):
        if self.startup_flow():
            self.logged_in = True
    else:
        return False


def encrypt_password(self, password):
    key = get_random_bytes(32)
    iv = get_random_bytes(12)
    time = int(datetime.datetime.now().timestamp())

    pubkey = base64.b64decode(self.publickey)

    rsa_key = RSA.importKey(pubkey)
    rsa_cipher = PKCS1_v1_5.new(rsa_key)
    encrypted_key = rsa_cipher.encrypt(key)

    aes = AES.new(key, AES.MODE_GCM, nonce=iv)
    aes.update(str(time).encode('utf-8'))

    encrypted_password, cipher_tag = aes.encrypt_and_digest(bytes(password, 'utf-8'))

    encrypted = bytes([1,
        self.publickeyid,
        *list(iv),
        *list(struct.pack('<h', len(encrypted_key))),
        *list(encrypted_key),
        *list(cipher_tag),
        *list(encrypted_password)])

    encrypted = base64.b64encode(encrypted).decode('utf-8')
    return f'#PWD_INSTAGRAM:4:{time}:{encrypted}'