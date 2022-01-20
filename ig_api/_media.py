def get_media_comments(self, media_id):
    request = self.get("media/{media_id}/comment_info/".format(media_id=media_id))
    return request


def like_media(self, media_id):
    like_data = {
        "delivery_class": "organic",
        "_uuid": self.device_id,
        "device_id": self.device_id,
        "_uid": self.ds_user_id,
        "is_carousel_bumped_post": False,
        "media_id": media_id,
        "nav_chain": self.create_nav_chain("IGMainFeedViewController"),
        "container_module": "feed_contextual_profile",
        "module_name": "feed_contextual_post",
        "carousel_index": "0"

    }

    request = self.post("media/{media_id}/like/?d=1".format(media_id=media_id), data=self.sign_json(like_data))

    return request
