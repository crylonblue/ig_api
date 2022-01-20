from . import constants


def convert_username_to_userid(self, username):
    request = self.search_username(username)
    if request:
        return str(request["user"]["pk"])
    else:
        return None


def get_user_feed(self, user_id):
    params = {
        "session_id": self.session_id,
        "seen_organic_items": self.simulate_seen_organic_items(),
        "source": "grid",
        "exclude_comment": True
    }

    return self.get("feed/user/{}/".format(user_id), params=params)


def get_user_info(self, user_id):
    params = {
        "device_id": self.device_id
    }

    return self.get("users/{}/info/".format(user_id), params=params)


def get_user_story(self, user_id):
    params = {
        "supported_capabilities_new": constants.SUPPORTED_CAPABILITIES
    }

    return self.get("feed/user/{}/story/".format(user_id), params=params)


def get_user_highlights(self, user_id):
    params = {
        "supported_capabilities_new": constants.SUPPORTED_CAPABILITIES
    }

    return self.get("highlights/{}/highlights_tray/".format(user_id), params=params)


def get_friendship(self, user_id):
    return self.get("friendships/show/{}/".format(user_id))


def search_username(self, username):
    response = self.get("users/" + username + "/usernameinfo/")

    if response.status_code == 200:
        return self.get_json(response)
    else:
        return None


def follow(self, user_id):
    follow_data = {
        "_uuid": self.device_id,
        "_uid": self.ds_user_id,
        "user_id": user_id,
        "device_id": self.device_id,
        "container_module": "newsfeed_you"
    }

    request = self.post("friendships/create/{}/".format(user_id), data=self.sign_json(follow_data))

    return request
