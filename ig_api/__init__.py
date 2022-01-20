from .constants import *
from ._logging_client_events import logging_client_events

class ig_api:
    from ._app import startup_app, startup_flow, prelogin_flow, get_client_time
    from ._user import convert_username_to_userid, get_user_feed, get_user_info, get_user_story, get_user_highlights, get_friendship, search_username, follow
    from ._feed import get_timeline, get_video_feed, log_feed_suggestion, simulate_feed_view_info, timeline_pull_to_refresh, simulate_seen_organic_items, pull_to_refresh, log_timeline_events
    from ._login import setup_logged_in_headers, setup_prelogin_headers, login, encrypt_password, relogin
    from ._session import restore_from_session_file, save_session_ids, save_login_session, save_claim, delete_session, generate_new_session_ids, generate_new_uuids, generate_random_uuid, get_seed
    from ._requests import check_request_status, check_set_headers, post, get, set_proxy, get_json, sign_json, update_pigeon_time
    from ._reels import get_all_seen_reels, get_all_organice_seen_reels, get_seen_sponsored_reels, simulate_viewing_reels, inject_ad_reels, get_reels_media, refresh_reels
    from ._direct import send_text_message, create_thread, send_text_message_to_userid, send_text_message_to_username, get_inbox, get_presence
    from ._search import register_recent_search_click, topsearch, get_search_dynamic_sections
    from ._misc import graphql_get_doc, get_topical_explore, random_batch, post_mobile_config, register_to_push, get_viewable_statuses, notifications_badge, sync, sync_launcher, discover_ayml, update_locale, create_nav_chain
    from ._media import get_media_comments, like_media
    from ._news import get_news, mark_news_seen
    from ._logging import log

    def __init__(self, username, password, proxy=None):
        self.username = username
        self.password = password
        self.session_id_lifetime = 1200000
        self.timeline = []
        self.timeline_last_fetch_time = self.get_client_time()
        self.reels = []
        self.ad_reels = []
        self.media_reels = []
        self.video_feed = []
        self.explore = []
        self.inbox = []
        self.proxy = proxy if proxy else ""
        self.session_file = "sessions/" + self.username + "_session.json"
        self.log_file = "sessions/logs/" + self.username + "_log.txt"
        self.status = "initializing"
        self.logged_in = False
        self.logging_client_events = logging_client_events(self)
