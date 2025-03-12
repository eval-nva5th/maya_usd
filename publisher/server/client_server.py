import socketio
import os
import threading

sio = socketio.Client()

@sio.event
def connect():
    print("ShotGrid Webhook Server Connected")

@sio.event
def disconnect():
    print("ShotGrid Webhook Server Disonnected")

@sio.on("shotgrid_notification")
def on_notification(data):
    print(data)
    message_dict = data.get("message_dict", "Someone published")
    project_name = message_dict['project_name']
    published_file_name = message_dict['published_file_name']
    created_by = message_dict['created_by']
    created_at = message_dict['created_at']
    message_text = f"{created_by} published {project_name} - {published_file_name} ({created_at})"
    print(message_text)
    os.system(f'notify-send "ShotGrid Notice" "{message_text}"')


def connect_to_server():
    print("Client Server Running")
    try:
        sio.connect("http://192.168.5.18:6000")
        sio.wait()
    except Exception as e:
        print(f"Server connect failed: {e}")

def run_client_in_thread():
    thread = threading.Thread(target=connect_to_server)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    connect_to_server()
else:
    run_client_in_thread()