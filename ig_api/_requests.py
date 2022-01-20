from . import constants
import requests
import time
import base64
import random
import urllib
import json
import zstd



def check_request_status(self, request):
    if request.status_code == 403:
        self.status = "unauthorized"
        self.log("got unauthorized from: {}".format(self.username))
        self.log(request.content)

        if self.logged_in:
            self.logged_in = False
            self.delete_session()

    if self.logged_in and request.status_code == 429:
        self.status = "too_many_requests"
        self.log("GOT 429, too many requests")

    if request.status_code == 400:

        self.log(request.content)
        json_response = json.loads(request.text)

        if json_response["message"] == "challenge_required":
            self.logged_in = False
            self.status = "challenge"
            if self.logged_in:
                self.delete_session()
        elif json_response["message"] == "feedback_required":
            self.status = "feedback_required"


def check_set_headers(self, request):
    if "x-ig-set-www-claim" in request.headers:
        if self.claim != request.headers["x-ig-set-www-claim"]:
            self.save_claim(request.headers["x-ig-set-www-claim"])
        self.claim = request.headers["x-ig-set-www-claim"]
        self.headers["x-ig-www-claim"] = str(self.claim)
        self.session.headers.update(self.headers)

    if "ig-set-ig-u-shbid" in request.headers:
        self.headers["ig-u-shbid"] = request.headers["ig-set-ig-u-shbid"]
        self.session.headers.update(self.headers)

    if "ig-set-ig-u-shbts" in request.headers:
        self.headers["ig-u-shbts"] = request.headers["ig-set-ig-u-shbts"]
        self.session.headers.update(self.headers)

    if "ig-set-ig-u-ig-direct-region-hint" in request.headers:
        self.headers["ig-u-ig-direct-region-hint"] = request.headers["ig-set-ig-u-ig-direct-region-hint"]
        self.session.headers.update(self.headers)

    if "ig-set-ig-u-rur" in request.headers:
        self.u_rur = request.headers["ig-set-ig-u-rur"]
        self.headers["ig-u-rur"] = self.u_rur
        self.session.headers.update(self.headers)

    if "ig-set-password-encryption-pub-key" in request.headers:
        self.publickey = request.headers["ig-set-password-encryption-pub-key"]

    if "ig-set-password-encryption-key-id" in request.headers:
        self.publickeyid = int(request.headers["ig-set-password-encryption-key-id"])


def post(self, endpoint, data=None, headers=None, version=1):
    try:
        if headers:
            self.session.headers.update(headers)

        self.update_pigeon_time()

        api_url = constants.API_URL if version == 1 else constants.API_URL_V2

        post_request = self.session.post(api_url + endpoint, data=data)

        self.log("[POST][{}] {} - {}".format(self.username, post_request.status_code, endpoint))

        self.check_set_headers(post_request)

        self.check_request_status(post_request)

        return post_request

    except Exception as e:
        self.log("[ERROR][{}] - {}".format(self.username, endpoint))
        self.log(e)
        return False


def get(self, endpoint, params=None, headers=None):
    try:
        if headers:
            self.session.headers.update(headers)

        self.update_pigeon_time()

        get_request = self.session.get(constants.API_URL + endpoint, params=params)

        self.log("[GET][{}] {} - {}".format(self.username, get_request.status_code, endpoint))

        self.check_set_headers(get_request)

        self.check_request_status(get_request)

        return get_request
    except:
        self.log("[ERROR][{}] - {}".format(self.username, endpoint))
        return False


def set_proxy(self, proxy):
    self.log("[INFO] set proxy {}".format(proxy))
    self.session.proxies["http"] = proxy
    self.session.proxies["https"] = proxy


def get_json(self, request):
    if request:
        try:
            #zstd compression
            if request.content.startswith(b"\x28\xb5\x2f\xfd"):
                return json.loads(zstd.decompress(request.content))
            else:
                return json.loads(request.text)
        except Exception as e:
            self.log("[ERROR] While trying to parse json")
            self.log(e)
            return request.content
    return False


def sign_json(self, raw_data):
    return "signed_body=SIGNATURE." + urllib.parse.quote_plus(json.dumps(raw_data, separators=(',', ':')))

def update_pigeon_time(self):
    self.headers["x-pigeon-rawclienttime"] = self.get_client_time()
    self.session.headers.update(self.headers)
