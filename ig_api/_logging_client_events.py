import zlib
import json
import requests
import base64
import time
import random
from . import constants


class logging_client_events:
    def send_logs_compressed(self):
        self.send_log(self.create_log_message(), True)

    def send_logs_uncompressed(self):
        self.send_log(self.create_log_message(), False)

    def add_log(self, log_name):
        self.message.append(log_name)
        self.push_if_ready()

    def push_if_ready(self):
        if len(self.message) > random.randint(4, 12):
            self.send_logs_compressed()
            self.message = []

    def send_log(self, message_dict, compression=False):
        data = {
            "format": "json",
            "access_token": constants.APP_ID + "|" + constants.ACCESS_TOKEN,
            "sent_time": self.api.get_client_time(),
            "system_uptime": self.get_system_uptime()
        }

        if compression:
            compressed_message = base64.b64encode(zlib.compress(bytes(json.dumps(message_dict).encode()), 1)).decode()
            data["compressed"] = 1
            data["message"] = compressed_message
        else:
            data["message"] = json.dumps(message_dict)

        try:
            log_request = self.session.post("https://graph.instagram.com/logging_client_events", data=data)
            self.api.log("[LOG][POST] {} - logging_client_events".format(log_request.status_code))
            self.seq += 1
        except:
            self.api.log("[LOG][ERROR] while logging client events")


    def create_log_message(self):
        log_message = {
            "data": self.message,
            "app_id": "124024574287414",
            "channel": "regular",
            "time": time.time(),
            "app_ver": "197.0.0.20.119 (305020938)",
            "device_id": self.api.device_id,
            "family_device_id": self.api.device_id,
            "session_id": self.api.pigeon_session_id,
            "log_type": "client_event",
            "app_uid": self.api.ds_user_id,
            "seq": self.seq
        }

        return log_message

    def get_random_log_time(self):
        return time.time() - random.uniform(2, 10)

    def get_system_uptime(self):
        return int(time.time() - self.system_start_time)

    def get_instagram_ad_delivery_log(self, m_pk, tracking_token, a_pk, ad_id):
        return {
            "extra": {
                "follow_status": "not_following",
                "media_loading_progress": 0,
                "m_pk": m_pk,
                "source_of_action": "feed_timeline",
                "tracking_token": tracking_token,
                "a_pk": a_pk,
                "is_dark_mode": self.api.is_dark_mode,
                "ad_id": ad_id,
                "radio_type": "wifi-none",
                "delivery_flags": "n"
            },
            "tags": 0,
            "module": "feed_time_line",
            "name": "instagram_ad_delivery",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_main_feed_request_succeed_log(self, reason, media_ids, feed_ranking_session_id, feed_ranking_request_id):
        unseen_indexes = [0, 1, 2, 3, 4, 5, 6]
        fetch_action = "reload"
        if reason == "pagination":
            fetch_action = "load_more"
        return {
            "extra": {
                "last_fetch_time": self.api.timeline_last_fetch_time,
                "has_unshown_items": False,
                "blocked_reason": "not_blocked",
                "radio_type": "wifi-none",
                "view_will_appear": False,
                "has_new_items": False,
                "application_state": "active",
                "application_will_become_active": False,
                "view_info_count": 0,
                "startup_origin": "normal",
                "media_ids": media_ids,
                "unseen_indexes": unseen_indexes,
                "is_onscreen": True,
                "current_module": "feed_timeline",
                "request_duration": random.randint(500, 2000),
                "view_did_appear": True,
                "feed_ranking_session_id": feed_ranking_session_id,
                "interaction_events": [],
                "reason": reason,
                "fetch_action": fetch_action,
                "new_items_delivered": False,
                "feed_ranking_request_id": feed_ranking_request_id,
                "time_since_background": 0,
                "pk": self.api.ds_user_id
            },
            "tags": 0,
            "module": "feed_time_line",
            "name": "ig_main_feed_request_succeeded",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_reel_tray_impression(self, story_ranking_token, reel_id):
        return {
            "extra": {
                "is_live_streaming": False,
                "is_new_reel": 1,
                "radio_type": "wifi-none",
                "viewed_reel_count": 0,
                "unfetched_reel_count": 0,
                "live_reel_count": 0,
                "tray_position": 0,
                "new_reel_count": 9,
                "is_besties_reel": False,
                "viewed_replay_reel_count": 0,
                "story_ranking_token": story_ranking_token,
                "has_my_reel": True,
                "new_replay_reel_count": 0,
                "tray_session_id": self.api.tray_session_id,
                "muted_live_reel_count": 0,
                "reel_age": 0,
                "has_my_replay_reel": False,
                "reel_label_type": "timestamp",
                "is_pride_reel": False,
                "pk": self.api.ds_user_id,
                "a_pk": reel_id,
                "reel_type": "story",
                "muted_replay_reel_count": 0,
                "reel_id": reel_id,
                "muted_reel_count": 0
            },
            "tags": 0,
            "module": "feed_time_line",
            "name": "reel_tray_impression",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_reel_tray_refresh_log(self):
        return {
            "extra": {
                "viewed_reel_count": 0,
                "was_successful": True,
                "tray_refresh_time": random.uniform(0.5, 2),
                "new_replay_reel_count": 0,
                "tray_refresh_type": "network",
                "tray_session_id": self.api.tray_session_id,
                "unfetched_reel_count": 0,
                "has_my_replay_reel": False,
                "story_ranking_token": self.api.reels["story_ranking_token"],
                "live_reel_count": 0,
                "pk": "48634776751",
                "muted_replay_reel_count": 0,
                "has_my_reel": False,
                "muted_reel_count": 0,
                "muted_live_reel_count": 0,
                "radio_type": "wifi-none",
                "new_reel_count": 0,
                "viewed_replay_reel_count": 0
            },
            "tags": 0,
            "module": "feed_timeline",
            "name": "reel_tray_refresh",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_database_create_log(self):
        return {
            "extra": {
                "success": True,
                "radio_type": "wifi-none",
                "pk": self.api.ds_user_id
            },
            "tags": 0,
            "module": "ig_sqlite_kit",
            "name": "sqlite_database_create",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def ig_remove_invalid_drafts_log(self):
        return {
            "extra": {
                "pk": self.api.ds_user_id,
                "invalid_drafts_count": 0,
                "radio_type": "wifi-none"
            },
            "tags": 0,
            "module": "ig_creation_draft",
            "name": "ig_remove_invalid_drafts",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_feed_view_info_enabled_log(self):
        return {
            "extra": {
                "enabled": True,
                "radio_type": "wifi-none",
                "pk": self.api.ds_user_id
            },
            "tags": 1,
            "module": "app",
            "name": "ig_ios_main_feed_view_info_enabled",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_fb_token_access_control_log(self):
        return {
            "extra": {
                "event_type": "token_access",
                "pk": self.api.ds_user_id,
                "caller_class": "IGMainFeedNetworkSourceRequestConfig",
                "caller_name": "ig_ios_feed_network_source_core",
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "app",
            "name": "fx_legacy_fb_token_on_ig_access_control",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_badging_event_log(self):
        return {
            "extra": {
                "radio_type": "wifi-none",
                "use_case_id": "profile",
                "event_type": "impression",
                "badge_value": 0,
                "badge_position": "bottom_navigation_bar",
                "badge_display_style": "dot_badge",
                "pk": self.api.ds_user_id
            },
            "tags": 1,
            "module": "app",
            "name": "badging_event",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_instagram_stories_request_sent_log(self, request_id):
        return {
            "extra": {
                "app_session_id": self.api.session_id,
                "tray_session_id": self.api.tray_session_id,
                "request_type": "cold_start",
                "request_id": request_id,
                "pk": "48634776751",
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "reel_feed_timeline",
            "name": "instagram_stories_request_sent",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_instagram_stories_request_completed_log(self, request_id):
        return {
            "extra": {
                "app_session_id": self.api.session_id,
                "tray_session_id": self.api.tray_session_id,
                "request_id": request_id,
                "request_type": "cold_start",
                "pk": self.api.ds_user_id,
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "reel_feed_timeline",
            "name": "instagram_stories_request_completed",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_instagram_organic_impression_log(self, feed_request_id, follow_status, media_pk, media_type, tracking_token, a_pk):
        return {
            "extra": {
                "session_id": self.api.ds_user_id + "_" + self.api.session_id,
                "feed_request_id": feed_request_id,
                "inventory_source": "media_or_ad",
                "media_loading_progress": 0,
                "follow_status": follow_status,
                "radio_type": "wifi-none",
                "nav_chain": "IGMainFeedViewController:feed_timeline:{}".format(random.randint(1, 4)),
                "action": "feed_timeline",
                "application_state": "active",
                "m_pk": media_pk,
                "m_t": media_type,
                "is_dark_mode": self.api.is_dark_mode,
                "tracking_token": tracking_token,
                "current_module": "feed_timeline",
                "is_checkout_enabled": False,
                "source_of_action": "feed_timeline",
                "pk": self.api.ds_user_id,
                "delivery_flags": "n",
                "m_ix": random.randint(0, 10),
                "a_pk": a_pk,
                "two_measurement_debugging_fields": {}
            },
            "tags": 1,
            "module": "feed_time_line",
            "name": "instagram_organic_impression",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_organic_impression_viewed_log(self, follow_status, m_pk, request_id, m_t, a_pk, session_id):
        return {
            "extra": {
                "follow_status": follow_status,
                "m_ix": random.randint(0, 10),
                "media_loading_progress": 3,
                "m_pk": m_pk,
                "application_state": "active",
                "source_of_action": "feed_timeline",
                "tracking_token": tracking_token,
                "inventory_source": "media_or_ad",
                "feed_request_id": request_id,
                "m_t": m_t,
                "a_pk": a_pk,
                "is_dark_mode": "1",
                "pk": self.api.ds_user_id,
                "session_id": session_id,
                "is_igtv": True,
                "delivery_flags": "n",
                "radio_type": "wifi-none"
            },
            "tags": 32,
            "module": "feed_timeline",
            "name": "instagram_organic_viewed_impression",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_navigation_tab_log(self):
        return {
            "extra": {
                "tabs": [
                    "main_home",
                    "main_search",
                    "main_camera",
                    "main_inbox",
                    "main_profile"
                ],
                "pk": self.api.ds_user_id,
                "headers": [],
                "app_start_type": "",
                "app_device_id": self.api.device_id,
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "app",
            "name": "ig_navigation_tab_impression",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_comment_impression_log(self, like_count, ca_pk, parent_c_pk, a_ck, m_pk):
        return {
            "extra": {
                "radio_type": "wifi-none",
                "like_count": like_count,
                "ca_pk": ca_pk,
                "is_covered": False,
                "parent_c_pk": parent_c_pk,
                "e_counter_channel": "",
                "a_pk": a_ck,
                "m_pk": m_pk,
                "c_pk": 17941748713535197,
                "pk": self.api.ds_user_id
            },
            "tags": 1,
            "module": "feed_timeline",
            "name": "comment_impression",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_instagram_organic_time_spent_log(self, m_pk, tracking_token, feed_request_id, m_t, a_pk, feed_session_id):
        random_timespent = random.uniform(1, 5)
        random_timespent_ms = int(random_timespent * 1000)
        return {
            "extra": {
                "follow_status": "following",
                "m_ix": random.randint(0, 10),
                "timespent": random_timespent,
                "m_pk": m_pk,
                "application_state": "active",
                "source_of_action": "feed_timeline",
                "timespent_in_ms": random_timespent_ms,
                "tracking_token": tracking_token,
                "inventory_source": "media_or_ad",
                "feed_request_id": feed_request_id,
                "m_t": m_t,
                "feed_ts_source": "new_fmk",
                "a_pk": a_pk,
                "is_dark_mode": self.api.is_dark_mode,
                "session_id": feed_session_id,
                "radio_type": "wifi-none",
                "pk": self.api.ds_user_id
            },
            "tags": 0,
            "module": "feed_timeline",
            "name": "instagram_organic_time_spent",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_video_displayed_log(self, like_count, ca_pk, parent_c_pk, a_pk, m_pk, c_pk, pk):
        return {
            "extra": {
                "radio_type": "wifi-none",
                "like_count": like_count,
                "ca_pk": ca_pk,
                "is_covered": False,
                "parent_c_pk": parent_c_pk,
                "e_counter_channel": "",
                "a_pk": a_pk,
                "m_pk": m_pk,
                "c_pk": c_pk,
                "pk": pk
            },
            "tags": 1,
            "module": "feed_timeline",
            "name": "comment_impression",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_direct_inbox_fetch_success_log(self, fetch_reason="cold_start"):
        return {
            "extra": {
                "action": "attempt",
                "radio_type": "wifi-none",
                "fetch_uuid": self.api.device_id,
                "fetch_type": "snapshot",
                "fetch_reason": fetch_reason,
                "pk": self.api.ds_user_id,
                "page_size": "20"
            },
            "tags": 0,
            "module": "ig_direct",
            "name": "ig_direct_inbox_fetch_success_rate",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_graphql_subscription_log(self):
        return {
            "extra": {
                "event_type": "client_subscribe",
                "ig_user_id": self.api.ds_user_id,
                "mqtt_subtopic": "1/graphqlsubscriptions/17867973967082385/{\"input_data\":{\"user_id\":\"" + str(self.api.ds_user_id) + "\"}}",
                "pk": self.api.ds_user_id,
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "app",
            "name": "ig_graphql_subscription_event",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_sso_status_log(self):
        return {
            "extra": {
                "containermodule": "waterfall_log_in",
                "pk": self.api.ds_user_id,
                "enabled": "NO",
                "enable_igid": self.api.ds_user_id,
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "app",
            "name": "sso_status",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_autocomplete_store_load_users_log(self):
        return {
            "extra": {
                "pk": self.api.ds_user_id,
                "current_user": "not_nil",
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "app",
            "name": "autocomplete_store_load_users",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def get_location_event_log(self):
        return {
            "extra": {
                "pk": self.api.ds_user_id,
                "ls_state": "OFF",
                "precise": True,
                "reason": "NOT_DETERMINED",
                "radio_type": "wifi-none"
            },
            "tags": 1,
            "module": "IGLocationKit",
            "name": "location_state_event",
            "time": self.get_random_log_time(),
            "sampling_rate": 1
        }

    def __init__(self, api):
        self.session = requests.Session()
        self.api = api
        self.system_start_time = time.time() - random.randint(10000, 100000)
        self.access_token = self.api.get_seed()
        self.session.headers.update({
            "user-agent": constants.USER_AGENT,
            "x-ig-bandwidth-speed-kbps": "0.000",
            "accept-language": "de-DE;q=1.0",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd, gzip, deflate",
            "x-fb-http-engine": "Liger",
            "x-fb-client-ip": "True",
            "x-fb-server-cluster": "True"
        })
        self.seq = 2
        self.event_count = 1
        self.api = api
        self.message = []
