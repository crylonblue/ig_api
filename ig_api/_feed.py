from . import constants
import random


def pull_to_refresh(self):
    # simulate pull refresh in app
    self.timeline_pull_to_refresh()
    self.refresh_reels("pull_to_refresh")


def timeline_pull_to_refresh(self):
    self.get_timeline(reason="pull_to_refresh")


def get_timeline(self, reason="cold_start_fetch"):
    # reasons: cold_start_fetch, pull_to_refresh, pagination

    timeline_data = {
        "is_async_ads_double_request": "0",
        "session_id": self.ds_user_id + "_" + self.session_id,
        "_uuid": self.device_id,
        "X-CM-Latency": "6000",
        "device_id": self.device_id,
        "is_async_ads_rti": "0",
        "has_seen_aart_on": "0",
        "request_id": self.ds_user_id + "_" + self.generate_random_uuid(),
        "rti_delivery_backend": "0",
        "X-CM-Bandwidth-KBPS": str(random.randint(7000, 10000)),
        "battery_level": random.randint(10, 100),
        "is_dark_mode": self.is_dark_mode,
        "is_charging": self.is_charging,
        "will_sound_on": "0",
        "timezone_offset": "7200",
        "bloks_versioning_id": constants.BLOKS_VERSION,
        "reason": reason,
        "att_permission_status": "2",
        "phone_id": self.device_id,
        "is_async_ads_in_headload_enabled": "0"
    }

    if reason != "cold_start_fetch":
        timeline_data["feed_view_info"] = self.simulate_feed_view_info()
        timeline_data["seen_organic_items"] = self.simulate_seen_organic_items()
        # self.logging_client_events.add_log(self.logging_client_events.get_main_feed_request_succeed_log())
    else:
        timeline_data["feed_view_info"] = "[]"

    if reason == "pull_to_refresh":
        timeline_data["is_pull_to_refresh"] = "1"

    timeline_request = self.post("feed/timeline/", data=timeline_data)

    if timeline_request:
        if timeline_request.status_code == 200:
            self.timeline = self.get_json(timeline_request)
            self.timeline_last_time_fetch = self.get_client_time()
            self.log_timeline_events(timeline_request)
            return timeline_request
        else:
            self.log(timeline_request.content)
            return False
    else:
        return False


def get_video_feed(self):
    data = {
        "tab_type": "clips_tab",
        "session_id": self.session_id,
        "_uuid": self.device_id,
        "container_module": "clips_viewer_clips_tab",
        "pct_reels": "0"
    }

    request = self.post("discover/videos_feed/", data=data)

    self.video_feed = self.get_json(request)

    return request


def log_feed_suggestion(self, action="seen"):
    log_data = {
        "is_business": "0",
        "_uuid": self.device_id,
        "type": "feed_aysf",
        "position": "4",
        "action": action
    }

    return self.post("feedsuggestion/log/", data=log_data)


def simulate_feed_view_info(self):
    # we simulate that we've seen every element in the feed
    feed_view_info = []
    if "feed_items" in self.timeline:
        for feed_item in self.timeline["feed_items"]:

            if "media_or_ad" in feed_item:
                item = feed_item["media_or_ad"]
                ts = item["taken_at"]
                media_id = str(item["id"]).split("_")[0]
                time_info = {"50": random.randint(150, 3000)}
                feed_view_info.append({
                    "media_id": media_id,
                    "ts": ts,
                    "media_pct": 1,
                    "time_info": time_info
                })

    return feed_view_info


def simulate_seen_organic_items(self):
    # we simulate that we've seen every element of the timeline
    seen_organic_items = []
    if "feed_items" in self.timeline:
        for feed_item in self.timeline["feed_items"]:
            if "media_or_ad" in feed_item:
                item = feed_item["media_or_ad"]
                timestamp = item["device_timestamp"]
                item_id = item["id"]

                seen_organic_items.append({
                    "item_id": item_id,
                    "seen_states": [{
                        "media_id": item_id,
                        "media_time_spent": [random.randint(150, 2000), random.randint(150, 2000),
                                             random.randint(150, 2000), random.randint(150, 2000)],
                        "impression_timestamp": timestamp + random.randint(10, 30),
                        "media_percent_visible": random.uniform(0.8, 1) if random.uniform(0, 1) > 0.5 else 1
                    }]
                })

    return seen_organic_items


def log_timeline_events(self, timeline_request):
    timeline_request_data = self.get_json(timeline_request)
    if "feed_items" in timeline_request_data:
        for feed_item in timeline_request_data["feed_items"]:
            if "media_or_ad" in feed_item:
                request_id = timeline_request_data["request_id"]
                session_id = timeline_request_data["session_id"]
                follow_status = "not_following"
                m_pk = feed_item["media_or_ad"]["pk"]
                m_t = feed_item["media_or_ad"]["media_type"]
                tracking_token = feed_item["media_or_ad"]["organic_tracking_token"]
                if "user" in feed_item["media_or_ad"]:
                    a_pk = feed_item["media_or_ad"]["user"]["pk"]
                    if "friendship_status" in feed_item["media_or_ad"]["user"]:
                        if "following" in feed_item["media_or_ad"]["user"]["friendship_status"]:
                            if feed_item["media_or_ad"]["user"]["friendship_status"]["following"]:
                                follow_status = "following"
                    self.logging_client_events.add_log(
                        self.logging_client_events.get_instagram_organic_impression_log(request_id, follow_status,
                                                                                        m_pk, m_t, tracking_token,
                                                                                        a_pk))
                    self.logging_client_events.add_log(
                        self.logging_client_events.get_instagram_organic_time_spent_log(m_pk, tracking_token,
                                                                                        request_id, m_t, a_pk,
                                                                                        session_id))
