import json
import time
import multiprocessing
import requests
from websocket import create_connection
server = "127.0.0.1:8080"
print("Already registerd?. Yes or No")
registered = input()
if registered == "No":
    print("Register Client.")
    print("Type Username:")
    username = input()
    print("Choose Password:")
    password = input()
    requests.get("http://%s/register/%s/%s"%(server, username, password))
    print("Username: %s created."%(username))
print("Following options are available: users, login, logout, tweet, follow, mentions, hashtags, followers, following, tweets, timeline, exit")
logged_in = 0 #global login flag
client = None
thread = None
timeline = None
def listen():
    global timeline
    while True:
        message = client.recv()
        print("Receiving over websocket.")
        messageJson = json.loads(message)
        if not "SocketSuccess" in messageJson:
            if timeline:
                timeline["Timeline"].append(messageJson)
                print("Current Timeline Updated.")
                print(timeline)
        print(messageJson)

while True:
    command = input()
    if command == "exit":
        print("Exiting...")
        break
    elif command == "login":
        if logged_in == 1:
            print("Already logged in.")
        else:
            print("Enter username")
            username = input()
            print("Enter password")
            password = input()
            client = create_connection("ws://%s/websocket"%server, timeout=5000)
            logged_in = 1
            timeline = requests.get("http://%s/timeline/%s"%(server, username)).json()
            print("Your current timeline")
            print(timeline)
            thread = multiprocessing.Process(target = listen)
            thread.start()
            client.send(json.dumps({"Username": username, "Password": password, "login": True, "tweet": "null"}))
    elif command == "logout":
        if logged_in == 0:
            print("Already logged out.")
        else:
            logged_in = 0
            thread.terminate()
            client.close()
            print("Successfully logged out")
    elif command == "tweet":
        print("Type tweet:")
        tweet = input()
        client.send(json.dumps({"Username": username, "Password": password, "login": False, "tweet": tweet}))
    elif command == "follow":
        print("Whom to follow:")
        following = input()
        requests.get("http://%s/follow/%s/%s"%(server, username, following))
    elif command == "mentions":
        print("What mention to filter on:")
        mention = input()
        temp = requests.get("http://%s/mentions/%s"%(server, mention))
        print(temp.json())
    elif command == "hashtags":
        print("What hashtag to filter on:")
        hashtag = input()
        temp = requests.get("http://%s/hashtags/%s"%(server, hashtag))
        print(temp.json())
    elif command == "followers":
        temp = requests.get("http://%s/followers/%s"%(server, username))
        print(temp.json())
    elif command == "following":
        temp = requests.get("http://%s/followings/%s"%(server, username))
        print(temp.json())
    elif command == "tweets":
        temp = requests.get("http://%s/tweets/%s"%(server, username))
    elif command == "timeline":
        print(timeline)
    elif command == "users":
        temp = requests.get("http://%s/users/%s"%(server,username))
        print(temp.json())
    elif command == "retweet":
        print("Displaying timeline")
        print("Insert tweet number")
        number = int(input())
        retweet = json.dumps(timeline["Timeline"][number-1])
        client.send(json.dumps({"Username": username, "Password": password, "login": False, "tweet": retweet}))

    print("Choose one of the options: users, login, logout, tweet, follow, mentions, hashtags, followers, following, tweets, tweets, retweet, exit")
