#
#     Stone VK Bot Engine
#       [Stolar Studio]
#

import vk_api, configparser, time, random, os, os.path

ver = "0.1"

if not os.path.exists("SVKBE_settings.txt"):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "log-chat", "0")
    config.set("Settings", "token", "")
    with open("SVKBE_settings.txt", "w") as config_file:
        config.write(config_file)
    print("write token in settings file")
    exit()
    
if not os.path.exists("SVKBE_msg.txt"):
    config = configparser.ConfigParser()
    config.add_section("MSG")
    config.set("MSG", "hello", "hello.py")
    with open("SVKBE_MSG.txt", "w") as config_file:
        config.write(config_file)
        
if not os.path.exists("hello.py"):
    f = open("hello.py", "w")   
    f.write("print('HELLO WORLD')")
    f.close()
    
config = configparser.ConfigParser()
config.read("SVKBE_settings.txt")
log_chat = config.get("Settings", "log-chat")
token = config.get("Settings", "token")

print("\n Stone VK Bot Engine v"+ver)
print("\n[ BOT STARTED ]\n")

vk = vk_api.VkApi(token=token)
vk._auth_token()

def save_log_chat(mes):
    if str(log_chat) == "1":
        f = open("log_VKSB.txt", "a")
        f.write(mes+"\n")
        f.close()
        
def send_msg(mes):
    vk.method("messages.send", {"peer_id": id, "message": mes, "random_id": random.randint(1, 2147483647)})
    itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
    print("["+itsatime+"] VKSB :: "+mes)
    save_log_chat("["+itsatime+"] VKSB :: "+mes)
    
while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
            print("["+str(id)+"]=["+itsatime+"] :: "+body.lower())
            save_log_chat("["+str(id)+"]=["+itsatime+"] :: "+body.lower())
            try :
                config = configparser.ConfigParser()
                config.read("SVKBE_msg.txt")
                msg = config.get("MSG",body.lower())
                os.system("py "+msg+" >buf.txt")
                f = open("buf.txt", "r")
                send_msg(f.read())
                f.close()
            except:
                send_msg("[ ERROR ]")
    except Exception as E:
        print("ERROR")
        time.sleep(1)
