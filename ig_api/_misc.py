from . import constants
import random
import json


def graphql_get_doc(self, doc_id, variables=None):
    if variables is None:
        variables = {}
    graphql_params = {
        "locale": "de_DE",
        "doc_id": doc_id,
        "variables": json.dumps(variables)
    }

    response = self.get("wwwgraphql/ig/query/", params=graphql_params)

    return response


def get_topical_explore(self):
    topical_explore_params = {
        "include_fixed_destinations": True,
        "is_on_wifi": True if random.randint(1, 2) > 1 else False,
        "timezone_offset": "7200",
        "omit_cover_media": True,
        "session_id": self.session_id,
        "use_sectional_payload": "1",
        "reels_configuration": "hide_hero",
        "is_prefetch": True,
        "network_transfer_rate": "120.25"
    }

    request = self.get("discover/topical_explore/", params=topical_explore_params)

    self.explore = self.get_json(request)

    return request


def discover_ayml(self):
    data = {
        "_uuid": self.device_id,
        "paginate": True,
        "module": "self_profile",
        "num_media": random.randint(1, 5)
    }

    return self.post("discover/ayml/", data=data)


def random_batch(self):
    random_batch = random.choice(constants.BATCHES)

    batch_data = {
        "is_sdk": "0",
        "_uuid": self.device_id,
        "_uid": self.ds_user_id,
        "surfaces_to_queries": json.dumps({random_batch["id"]: constants.BATCH_QUERY}),
        "vc_policy": "default",
        "version": "1",
        "surfaces_to_triggers": json.dumps({random_batch["id"]: random.choice(random_batch["triggers"])}),
        "scale": "3.000000"
    }

    return self.post("qp/batch_fetch/", data=self.sign_json(batch_data))


def post_mobile_config(self):
    mobile_config = {
        "_uuid": self.device_id,
        "device_id": self.device_id,
        "_uid": self.ds_user_id,
        "bool_opt_policy": "0",
        "unit_type": "2",
        "fetch_type": "ASYNC_FULL",
        "query_hash": str(self.get_seed()) + str(self.get_seed()),
        "name_to_id": "true",
        "api_version": "3"
    }

    return self.post("launcher/mobileconfig/", data=self.sign_json(mobile_config))


def register_to_push(self, device_type, device_token):
    push_register_data = {
        "_uuid": self.device_id,
        "device_id": self.device_id,
        "device_token": device_token,
        "family_device_id": self.device_id,
        "device_app_installations": json.dumps({"threads": False, "igtv": False, "instagram": True}),
        "users": self.ds_user_id,
        "device_type": device_type
    }

    return self.post("push/register/?platform={platform_id}&device_type={device_type}".format(platform_id="18",
                                                                                              device_type=device_type),
                     data=push_register_data)


def get_viewable_statuses(self):
    params = {
        "include_authors": True
    }

    return self.get("status/get_viewable_statuses/", params=params)


def notifications_badge(self):
    data = {
        "user_ids": self.ds_user_id,
        "device_id": self.device_id,
        "_uuid": self.device_id
    }

    return self.post("notifications/badge/", data=data)


def sync(self):
    sync_data = {
        "id": self.ds_user_id,
        "_uuid": self.device_id,
        "_uid": self.ds_user_id,
        "server_config_retrieval": "1"
    }
    return self.post("qe/sync/", data=self.sign_json(sync_data))


def sync_launcher(self):
    sync_data = {
        "use_mc": "1",
        "id": self.ds_user_id,
        "_uuid": self.device_id,
        "_uid": self.ds_user_id,
        "server_config_retrieval": "1"
    }

    return self.post("launcher/sync/", data=self.sign_json(sync_data))


def update_locale(self):
    update_locale_data = {
        "locale": "",
        "_uuid": self.device_id,
        "_uid": self.ds_user_id
    }

    return self.post("users/update_user_locale/", data=update_locale_data)



def create_nav_chain(self, target):
    view_controllers = [
        {
            "name": "IGMainFeedViewController",
            "container_modules": [
                "feed_timeline"
            ]
        },
        {
            "name": "IGDirectInboxNavigationController",
            "container_modules": [
                "direct_inbox"
            ]
        },
        {
            "name": "IGDirectThreadViewController",
            "container_modules": [
                "direct_thread"
            ]
        },
        {
            "name": "IGProfileViewController",
            "container_modules": [
                "profile"
            ]
        },
        {
            "name": "IGContextualFeedViewController",
            "container_modules": [
                "feed_contextual_profile"
            ]
        },
        {
            "name": "IGExploreViewController",
            "container_modules": [
                "explore_popular"
            ]
        }
    ]

    chain_action = random.randint(2, 6)
    nav_chain_string = ""
    for i in range(random.randint(2, 5)):
        view_controller = random.choice(view_controllers)
        nav_chain_string += "{}:{}:{},".format(view_controller["name"], random.choice(view_controller["container_modules"]), chain_action)
        chain_action += random.randint(2, 4)

    for view_controller in view_controllers:
        if view_controller["name"] == target:
            nav_chain_string += "{}:{}:{}".format(view_controller["name"], random.choice(view_controller["container_modules"]), chain_action)

    return nav_chain_string
