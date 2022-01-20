import requests
from . import constants
import time
import random
import json


def startup_app(self, device_id=None):
    # we are generating new session ids
    self.session = requests.session()
    self.claim = "0"

    # we are adding the default header
    # pass by value
    self.headers = dict(constants.HEADERS)
    self.session.headers.update(self.headers)

    # update the time for pigeon
    self.update_pigeon_time()

    # misc
    self.is_charging = random.randint(0, 1)

    # if we restore the session

    if self.restore_from_session_file():
        self.log("[INFO] login using session file")

        # set proxy to savefile
        self.set_proxy(self.proxy)

        if (time.time() - int(self.session_start)) > self.session_id_lifetime:
            self.log("[INFO] previous session elapsed, generate new session")
            self.generate_new_session_ids()
            self.save_session_ids()

        if self.startup_flow(fresh_login=False):
            self.logged_in = True

    else:
        self.log("[INFO] fresh login")

        # simulate new session
        self.session_start = time.time()
        self.generate_new_session_ids()

        # simulate new device
        self.generate_new_uuids()

        # if we have a device id preset
        if device_id:
            print("[INFO] setting up custom device id")
            self.device_id = device_id

        self.log(
            "[INFO] device_id: {device_id}\npigeon_session_id: {pigeon_session_id}\ndevice_token: {device_token}\nvoip_ios_token: {ios_voip_device_token}".format(
                device_id=self.device_id, pigeon_session_id=self.pigeon_session_id, device_token=self.device_token,
                ios_voip_device_token=self.ios_voip_device_token))
        # set proxy
        self.set_proxy(self.proxy)
        # get public keys and set defaults
        if not self.prelogin_flow():
            self.log("[INFO] ERROR OCCURRED ON PRELOGIN FLOW")
            return False
        # login
        self.logged_in = self.login(self.username, self.password)

        if self.logged_in:
            self.startup_flow()

    if self.logged_in:
        self.log("[INFO] logged in {}!".format(self.username))
        self.status = "valid"
        return True
    else:
        self.status = "login_failure"
        try:
            self.delete_session()
        except:
            pass
        return False


def startup_flow(self, fresh_login=True):
    self.sync()
    self.sync_launcher()
    interop_response = self.get("direct_v2/has_interop_upgraded")

    if interop_response:
        if interop_response.status_code != 200:
            if interop_response.status_code == 403:
                response_json = self.get_json(interop_response)
                if "message" in response_json:
                    if response_json["message"] == "login_required" and response_json["logout_reason"] == 8:
                        self.relogin()
                        return False
            else:
                return False
    else:
        return False

    if not fresh_login:
        self.post_mobile_config()

    self.get("qp/get_cooldowns/")
    self.get_timeline()
    self.refresh_reels()
    self.graphql_get_doc("3323463714396709", {"include_fbpay_enabled": True, "include_fbpay_is_connected": False})

    if not fresh_login:
        self.graphql_get_doc("2796210233799562")
        self.graphql_get_doc("2476027279143426")
        self.get("pro_home/badge_pro_home_entry_point/")
        self.get("archive/reel/profile_archive_badge/?timezone_offset=7200")
        self.get_news()

    self.get_inbox()

    self.notifications_badge()

    # self.register_to_push("ios", self.device_token)
    # self.register_to_push("ios_voip", self.device_token)

    if not fresh_login:
        self.discover_ayml()

    self.get("multiple_accounts/get_account_family/")

    business_eligibility_params = {
        "product_types": "branded_content,igtv_revshare,user_pay"
    }

    self.get("business/eligibility/get_monetization_products_eligibility_data/", params=business_eligibility_params)

    self.get("business/branded_content/should_require_professional_account/")

    camera_models_data = {
        "model_request_blobs": json.dumps([{
            "type": "nametag",
            "nametag_model_version": "1",
            "supported_model_compression_type": "TAR_BROTLI,NONE"
        }]),
        "_uuid": self.device_id,
        "_uid": self.ds_user_id
    }

    self.post("creatives/camera_models/", data=self.sign_json(camera_models_data))

    self.get("users/" + self.ds_user_id + "/info/?device_id=" + self.device_id)

    self.get("fbsearch/recent_searches/")

    banyan_params = {
        "views": json.dumps([
            "story_share_sheet",
            "direct_user_search_nullstate",
            "reshare_share_sheet",
            "group_stories_share_sheet",
            "forwarding_recipient_sheet",
            "share_extension",
            "direct_user_search_keypressed"
        ])
    }

    self.get("banyan/banyan/", params=banyan_params)

    self.get("civic_action/get_voting_feed_banner/")

    if fresh_login:
        self.get("profiling/client_network_trace_sampling/")

    self.get("linked_accounts/get_linkage_status_v2/")

    self.get("friendships/autocomplete_user_list/?version=2")

    bootstrap_params = {
        "surfaces": json.dumps([
            "coefficient_ios_section_test_bootstrap_ranking",
            "coefficient_besties_list_ranking",
            "coefficient_rank_recipient_user_suggestion",
            "autocomplete_user_list"
        ])
    }

    self.get("scores/bootstrap/users/", params=bootstrap_params)

    self.random_batch()

    if fresh_login:
        self.update_locale()

    if not fresh_login:
        self.get_topical_explore()

    self.logging_client_events.add_log(self.logging_client_events.get_fb_token_access_control_log())
    self.logging_client_events.add_log(self.logging_client_events.get_badging_event_log())
    self.logging_client_events.add_log(self.logging_client_events.get_navigation_tab_log())
    self.logging_client_events.add_log(self.logging_client_events.get_direct_inbox_fetch_success_log())

    if fresh_login:
        self.logging_client_events.add_log(self.logging_client_events.get_database_create_log())

    if random.random() < 0.5:
        self.logging_client_events.add_log(self.logging_client_events.get_graphql_subscription_log())

    self.logging_client_events.add_log(self.logging_client_events.get_sso_status_log())

    if random.random() < 0.5:
        self.logging_client_events.add_log(self.logging_client_events.get_autocomplete_store_load_users_log())

    self.logging_client_events.add_log(self.logging_client_events.get_location_event_log())

    return True


def prelogin_flow(self):
    self.log("[INFO] pre login flow ...")

    self.headers["x-device-id"] = self.device_id
    self.session.headers.update(self.headers)

    response = self.post("qe/sync/", data={
        "id": self.device_id,
        "server_config_retrieval": "1"
    })

    if not response:
        return False

    self.publickeyid = int(response.headers['ig-set-password-encryption-key-id'])
    self.publickey = response.headers["ig-set-password-encryption-pub-key"]

    if "ig-set-x-mid" in response.headers:
        self.mid = str(response.headers["ig-set-x-mid"])
    else:
        self.mid = "0"

    if "ig-set-authorization" in response.headers:
        self.auth = response.headers["ig-set-authorization"]

    self.ds_user_id = response.headers["ig-set-ig-u-ds-user-id"]
    self.ig_u_rur = response.headers["ig-set-ig-u-rur"]

    self.setup_prelogin_headers()

    return True


def get_client_time(self):
    return "%.6f" % time.time()
