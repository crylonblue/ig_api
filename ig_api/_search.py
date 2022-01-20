from . import constants

def register_recent_search_click(self, instagram_name, user_id):
    register_data = {
        "_uuid": self.device_id,
        "entity_type": "user",
        "entity_name": instagram_name,
        "entity_id": user_id
    }

    return self.post("fbsearch/register_recent_search_click/", data=register_data)


def topsearch(self, query):
    params = {
        "context": "blended",
        "query": query,
        "search_surface": "top_search_page",
        "is_typeahead": "true",
        "timezone_offset": "7200"
    }

    response = self.get("fbsearch/topsearch_flat/", params=params)

    if response:
        return response
    else:
        return False


def get_search_dynamic_sections(self):
    params = {
        "type": "blended",
        "rank_token": self.ds_user_id + "_" + self.generate_random_uuid()
    }

    response = self.get("fbsearch/nullstate_dynamic_sections/", params=params)

    return response

