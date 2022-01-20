import random
import json
import time

def send_text_message(self, thread_id, text):
    client_context = "".join(["{}".format(random.randint(0, 9)) for num in range(0, 19)])

    send_data = {
        "action": "send_item",
        "_uuid": self.device_id,
        "client_context": client_context,
        "device_id": self.device_id,
        "offline_threading_id": client_context,
        "mutation_token": client_context,
        "text": text,
        "thread_id": thread_id,
        "nav_chain": self.create_nav_chain("IGProfileViewController"),
        "send_attribution": "direct_inbox",
        "is_shh_mode": 0
    }

    return self.post("direct_v2/threads/broadcast/text/", data=send_data)

def create_thread(self, recipients):

    thread_context = self.generate_random_uuid()

    thread_data = {
        "client_context": thread_context,
        "_uuid": self.device_id,
        "recipient_users": json.dumps(recipients),
        "_uid": self.ds_user_id
    }

    thread_context = self.post("direct_v2/create_group_thread/", data=self.sign_json(thread_data))

    if thread_context.status_code == 200:
        thread_response_json = self.get_json(thread_context)
        thread_id = thread_response_json["thread_id"]

        return thread_id
    else:
        return None

def send_text_message_to_userid(self, user_id, text):

    thread_id  = self.create_thread([user_id])
    if thread_id:
        time.sleep(random.randint(2, 5))
        send_request = self.send_text_message(thread_id, text)

        if send_request.status_code == 200:
            return True

    return False

def send_text_message_to_username(self, username, text):
    try:
        user_id = self.convert_username_to_userid(username)

        if user_id:
            return self.send_text_message_to_userid(user_id, text)
    except Exception as e:
        self.log("[ERROR][{}] While sending message".format(self.username))
        self.log(e)
        
    return False

def get_inbox(self, reason="cold_start_fetch", cursor=None):
    #reasons: cold_start_fetch, pull_to_refresh, pagination

    inbox_params = {
        "persistentBadging": True,
        "folder": "0",
        "fetch_reason": reason,
        "thread_message_limit" : "10",
        "limit": "20"
    }

    if cursor != None:
        inbox_params["cursor"] = cursor

    inbox_request = self.get("direct_v2/inbox/", params=inbox_params)

    self.inbox = self.get_json(inbox_request)
    
    return inbox_request 


def get_presence(self, additional_params=False):
    if additional_params:   
        params = {
            "recent_thread_limit": "25",
            "suggested_followers_limit": "150"
        }
    else:
        params = None

    return self.get("direct_v2/get_presence/", params=params)
