# ig_api
##### instagram 1.97 / ios api wrapper

After 2 yrs of experience in instagram automation, i am putting my code, that i used open source. This is a basic api wrapper i used for automation. In the examples section you'll find a production ready bot-handler, that will handle unlimited bots. We had upto 200 accounts running on one instance. To use the scripts properly you'll have to get a proper accounts setup. While I could write a whole book about the right account setup here are a few tips.

1. Good proxy (never use more than five accounts on one proxy except if the proxy is really good)
2. Last location of login has to match the proxies location
3. Phone-Id, Phone have to be ideally the same, also the App-Version has to match
4. Do some manual actions, to build up your trust-score, which is connected to your device-id 

In the ideal case you fulfill all 4 requirements. In that case, the risk of getting your account banned is low (if you do not do crazy things - like 2000 messages/day)


# How to use:

install the package:
```bash
python3 setup.py install
```

create a new python file and send a message to a specific user.
```python
api = ig_api("username", "password", "proxy")
api.startup_app()
api.send_message_to_username("username", "text")
```

# Example

In the examples folder you'll find our setup we ran with over 200 accounts. To test this you'll have to login the accounts first. You'll have to create sessions, that can later be used by the bot_handler.py. To login accounts, you'll have to write the account information into the accounts.txt. I will go into further detail about this, since i requires much more experience to run a bigger instance.