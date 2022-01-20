
def get_news(self, max_id=None, first_record_timestamp=None):
        params = {
            "mark_as_seen": False,
            "timezone_offset": 7200
        }

        if max_id and first_record_timestamp:
            params = {
                "max_id": max_id,
                "last_checked": str(float(self.get_client_time()) - 30),
                "pagination_first_record_timestamp": first_record_timestamp,
                "mark_as_seen": False,
                "timezone_offset": 7200
            }

        request = self.get("news/inbox/", params=params)

        self.news = self.get_json(request)

        return request


def mark_news_seen(self):
    data = {
        "_uuid": self.device_id
    }

    return self.post("news/inbox_seen/")