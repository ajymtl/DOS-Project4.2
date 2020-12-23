# DOS (COP-5615) Project 4-2

## Information about files:
File Structure:
- Server (In f#, suave, websockets+rest)
- client.py (In python) (websockets, requests)

## How to run:
- Server: dotnet run
- Client: python3 client.py

## Implemented functionalities:
- Register. (REST)
- Login/Logout. (WebSocket)
- Get Timeline for a user. (REST for first time, WebSocket for streaming tweets)
- Tweet. (WebSocket)
- Get All Users. (REST)
- Get Followers for a user. (REST)
- Get All Users a person is Following. (REST)
- Get Tweets by a user. (REST)
- Get Mentions by a keyword. (REST)
- Get Hashtags by a keywordFollow a user. (REST)

## Workflow:
- A user registers using REST(over HTTP). Once registered, when the user logs in, a
websocket is created. Server stores websockets and login status of all users. Server
communicates all timeline updates through this websocket and user tweets using the
same websocket (hence, testing the duplex behavior).
- All other one time requests e.g. following someone etc. are done by REST(over HTTP).
