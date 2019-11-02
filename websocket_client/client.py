import websocket


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print('Connection Opened')
    ws.send('Can you hear me?')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.43.81:8999",
            on_message = on_message,
            on_error = on_error,
            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
