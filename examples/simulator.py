import random
import time
import string
import json
import os


class simulator:

    def simulate_scrolling(self):
        self.api.log("[SIMULATOR][{}] simulate viewing timeline".format(self.api.username))
        try:
            # do it 1 to 3 times
            for x in range(random.randint(1, 3)):
                self.api.get_timeline(reason="pagination")
                time.sleep(random.uniform(1, 3))
                self.api.log_feed_suggestion()
                time.sleep(random.uniform(5, 30))
        except Exception as e:
            self.api.log(e)
            self.api.log("[SIMULATOR][{}] Error, while simulate scrolling".format(self.api.username))

    def simulate_viewing_reels(self):
        self.api.log("[SIMULATOR][{}] simulate viewing reels".format(self.api.username))
        try:
            self.api.simulate_viewing_reels()
        except:
            self.api.log("[SIMULATOR][{}] Error, while viewing reels".format(self.api.username))

    def like_random_from_timeline(self):
        for feed_item in self.api.timeline["feed_items"]:
            if "media_or_ad" in feed_item:
                if random.random() > 0.7:
                    item_id = feed_item["media_or_ad"]["id"]
                    self.api.log("[SIMULATOR][{}] liking media with id {}".format(self.api.username, item_id))
                    self.api.like_media(item_id)

    def check_simulate_search_user(self, user_id, username):
        self.api.get_search_dynamic_sections()
        time.sleep(random.uniform(1, 3))
        step = int(len(username) / 3)
        self.api.topsearch(username[0:step])
        time.sleep(random.uniform(1, 3))
        self.api.topsearch(username[0:(step + step)])
        time.sleep(random.uniform(1, 3))
        final_search = self.api.topsearch(username)
        time.sleep(random.uniform(1, 3))

        if final_search:
            try:
                search_json = self.api.get_json(final_search)
                if "list" in search_json:
                    for entry in search_json["list"]:
                        if "user" in entry:
                            if str(entry["user"]["pk"]) == str(user_id):
                                return True
                self.api.log("[SIMULATOR][{}] user {} not found".format(self.api.username, username))
            except Exception as e:
                self.api.log(e)
                self.api.log("[SIMULATOR][{}] Error while searching".format(self.api.username))

        return False

    def simulate_show_user(self, user_id):
        user_info_request = self.api.get_user_info(user_id)
        if user_info_request:
            user_json = self.api.get_json(user_info_request)
            if user_json["user"]["is_private"] == False:
                self.api.get_user_feed(user_id)
            self.api.get_user_story(user_id)
            self.api.get_user_highlights(user_id)
            self.api.get_friendship(user_id)

    def simulate_random_search(self):
        self.api.log("[SIMULATOR][{}] simulate random search".format(self.api.username))
        self.api.get_search_dynamic_sections()
        time.sleep(random.uniform(1, 3))
        randomsearchstring = "".join(random.choice(string.ascii_letters) for i in range(random.randint(4, 9)))
        self.api.topsearch(randomsearchstring[random.randint(2, 3):])
        time.sleep(random.uniform(1, 3))

        last_search = self.api.topsearch(randomsearchstring)

        if last_search:
            try:
                search_json = self.api.get_json(last_search)
                if "list" in search_json:
                    if len(search_json["list"]) > 0:
                        first_user_pk = search_json["list"][0]["user"]["pk"]
                        first_user_name = search_json["list"][0]["user"]["username"]
                        time.sleep(random.uniform(2, 5))
                        self.api.register_recent_search_click(first_user_name, first_user_pk)
                        self.simulate_show_user(first_user_name)
            except Exception as e:
                self.api.log(e)
                self.api.log("[ERROR][{}] simulating random search".format(self.api.username))

    def __init__(self, api):
        self.api = api
