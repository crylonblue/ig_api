from ig_api import ig_api
import uuid


def convert_to_valid_uuid(uuid_test):
    try:
        uuid_obj = uuid.UUID(uuid_test, version=4)
    except ValueError:
        return False
    return str(uuid_obj)


verified_users = []
errors = []

print("Paste in account file:")
account_file = open(input(), "r")
lines = account_file.readlines()

for line in lines:
    line = line.split(",")
    user = line[0]
    password = line[1]
    device_id = line[2]
    proxy = line[3].replace('\n', '').replace('\r', '')

    login_bot = ig_api(user, password, proxy)

    if login_bot.startup_app(device_id=convert_to_valid_uuid(device_id)):
        verified_users.append(user)

print("Verified user:")
print(verified_users)
print("Failed:")
print(errors)
