from . import constants
import time
import random


def get_all_seen_reels(self):
    reels = {}

    for reel in self.reels["tray"]:
        user_id = reel["user"]["pk"]
        reel_id = reel["id"]
        latest_reel_media = reel["latest_reel_media"]
        if "media_ids" in reel:
            for media_id in reel["media_ids"]:
                unique_reel_id = str(media_id) + "_" + str(reel_id) + "_" + str(user_id)
                reels[unique_reel_id] = [str(latest_reel_media) + "_" + str(int(time.time()) - random.randint(10, 30))]

    return reels


def get_all_organice_seen_reels(self):
    organic_seen_reels = []

    for reel in self.reels["tray"]:
        item_id = reel["id"]
        seen_states = []

        for media_id in reel["media_ids"]:
            seen_states.append({
                "media_id": media_id,
                "media_time_spent": [random.randint(150, 3000)],
                "impression_timestamp": int(time.time()) - random.randint(10, 100),
                "media_percent_visible": 1
            })

        organic_seen_reels.append({
            "item_id": item_id,
            "seen_states": seen_states
        })

    return organic_seen_reels


def get_seen_sponsored_reels(self):
    seen_sponsored_reels = []
    for reel_id, reel_content in self.ad_reels["reels"].items():

        item_id = str(reel_content["id"]).split("_")[0]

        if "items" in reel_content:
            media_id = reel_content["items"][0]["id"]

            seen_sponsored_reels.append({
                "item_type": random.randint(2, 3),
                "inventory_source": "",
                "item_id": item_id,
                "seen_states": [{
                    "media_id": media_id,
                    "media_time_spent": [random.randint(150, 2500)],
                    "impression_timestamp": int(time.time()) - random.randint(10, 30),
                    "media_percent_visible": 1
                }]

            })

    return seen_sponsored_reels


def simulate_viewing_reels(self):
    try:
        self.log("[INFO][{}] simulate viewing stories".format(self.username))

        self.get_reels_media()

        self.log("[INFO][{}] got media reels".format(self.username))
        time.sleep(random.randint(2, 5))

        ad_reel_request = self.inject_ad_reels()

        self.ad_reels = self.get_json(ad_reel_request)

        self.log("[INFO][{}] got ad reels".format(self.username))

        time.sleep(random.randint(5, 10))

        seen_data = {
            "seen_sponsored_reels": self.get_seen_sponsored_reels(),
            "_uuid": self.device_id,
            "_uid": self.ds_user_id,
            "reels": self.get_all_seen_reels(),
            "live_vods_skipped": {},
            "skip_timestamp_update": "1",
            "live_vods": {},
            "container_module": "reel_feed_timeline",
            "reel_media_skipped": {},
            "seen_organic_reels": self.get_all_organice_seen_reels()
        }

        request = self.post("media/seen/?reel=1&live_vod=0&reel_skipped=0&live_vod_skipped=0",
                            data=self.sign_json(seen_data), headers=None, version=2)

        if request.status_code == 200:
            return True
        else:
            return False
    except Exception as e:

        self.log(e)
        self.log("[ERROR][{}] While simulate viewing reels".format(self.username))


def inject_ad_reels(self):
    post_data = {
        "is_media_based_enabled": "1",
        "_uuid": self.device_id,
        "_uid": self.ds_user_id,
        "ad_and_netego_request_information": [],
        "X-CM-Latency": "7.322",
        "ad_and_netego_realtime_information": [],
        "has_seen_aart_on": "0",
        "ad_request_index": "0",
        "is_inventory_based_request_enabled": "1",
        "is_ad_pod_enabled": "0",
        "X-CM-Bandwidth-KBPS": str(random.randint(7000, 10000)),
        "battery_level": random.randint(10, 100),
        "is_dark_mode": self.is_dark_mode,
        "tray_session_id": self.tray_session_id,
        "num_items_in_pool": "0",
        "is_charging": self.is_charging,
        "reel_position": "0",
        "viewer_session_id": self.generate_random_uuid(without_hyphen=True),
        "surface_q_id": "3303646759746658",
        "will_sound_on": "0",
        "tray_user_ids": [reel["user"]["pk"] for reel in self.reels["tray"]],
        "earliest_request_position": "0",
        "is_media_based_insertion_enabled": "1",
        "att_permission_status": "2",
        "phone_id": self.device_id,
        "entry_point_index": "0",
        "is_first_page": "1"
    }

    request = self.post("feed/injected_reels_media/", data=self.sign_json(post_data))

    return request


def get_reels_media(self):
    user_ids = [reel["user"]["pk"] for reel in self.reels["tray"]]
    self.reels_media_request_id = self.ds_user_id + "_" + self.generate_random_uuid()
    reels_media_data = {
        "user_ids": user_ids,
        "source": "feed_timeline_stories_netego",
        "_uuid": self.device_id,
        "tray_session_id": self.tray_session_id,
        "_uid": self.ds_user_id,
        "request_id": self.reels_media_request_id,
        "supported_capabilities_new": constants.SUPPORTED_CAPABILITIES,
        "inject_at_beginning": "0"
    }

    request = self.post("feed/reels_media/", data=self.sign_json(reels_media_data))
    self.reels_media = self.get_json(request)
    return request


def refresh_reels(self, reason="cold_start"):
    # reasons: cold_start, pagination, pull_to_refresh
    # feed/reels_tray/
    request_id = self.ds_user_id + "_" + self.generate_random_uuid()
    try:
        self.tray_session_id = self.generate_random_uuid(without_hyphen=True)
        reels_data = {
            "reason": reason,
            "_uuid": self.device_id,
            "tray_session_id": self.tray_session_id,
            "_uid": self.ds_user_id,
            "request_id": request_id,
            "supported_capabilities_new": constants.SUPPORTED_CAPABILITIES,
            "timezone_offset": "7200"
        }

        request = self.post("feed/reels_tray/", data=self.sign_json(reels_data))

        self.reels = self.get_json(request)
        self.logging_client_events.add_log(self.logging_client_events.get_reel_tray_refresh_log())
        self.logging_client_events.add_log(self.logging_client_events.get_instagram_stories_request_sent_log(request_id))
        self.logging_client_events.add_log(self.logging_client_events.get_instagram_stories_request_completed_log(request_id))
        return request
    except:
        self.log("[ERROR][{}] while fetching reels".format(self.username))
        return None
