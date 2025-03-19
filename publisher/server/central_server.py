from flask import Flask, request, jsonify
import shotgun_api3
from datetime import datetime, timezone, timedelta
import os
import threading
import socketio
import eventlet
from shotgridapi import ShotgridAPI
from systempath import SystemPath
sg = ShotgridAPI().shotgrid_connector()
root_path = SystemPath().get_root_path()

app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")  # 내부망에서 클라이언트 연결 허용
flask_app = socketio.WSGIApp(sio, app)

connected_clients = {}

@app.route("/notify", methods=["POST"])
def notify_maya():
    print("__________________________________________notify maya_______________________________________________")
    try:
        data = request.json.get("data", {})
        if not data:
            return jsonify({"error": "No data received"}), 400

        created_at = data.get("created_at", "")
        if created_at:
            created_at = convert_ktime(created_at)
        else:
            created_at = "Unknown Time"

        published_file_id = data.get("entity", {}).get("id")
        if not published_file_id:
            return jsonify({"error": "Invalid published file data"}), 400

        fields = ["code", "project", "created_by", "entity", "task", "sg_local_path"]
        published_file = sg.find_one("PublishedFile", [["id", "is", published_file_id]], fields)

        if not published_file:
            return jsonify({"error": "Published file not found"}), 404

        project_name = published_file["project"]["name"]
        task_data = published_file.get("task")
        
        if not task_data:
            return jsonify({"error": "No task linked to this file"}), 400

        task_id = task_data["id"]
        assignees_ip_list = get_assignees_ip(task_id)

        message_dict = {
            "task_id": task_id,
            "project_name": project_name,
            "published_file_name": published_file["code"],
            "created_by": published_file["created_by"]["name"],
            "created_at": created_at,
            "local_path" : published_file["sg_local_path"]
        }

        message_text = f"{message_dict['project_name']}  |  {message_dict['published_file_name']}  |  {message_dict['created_by']}  |  {message_dict['created_at']}"

        
        for ip in assignees_ip_list:
            sio.emit("shotgrid_notification", {"message_dict": message_dict}, room=ip)
            
            print(f"Sent signal to {ip}")

        for ip in assignees_ip_list:
            if ip in connected_clients:
                sid = connected_clients[ip]
                print(f"[DEBUG] Sending notification to {ip} (SID: {sid})")
                try:
                    sio.emit("shotgrid_notification", {"message_dict": message_dict}, room=sid)
                    print(f"[DEBUG] Successfully sent notification to {ip}")
                except Exception as e:
                    print(f"[DEBUG] Failed to send notification to {ip}: {e}")
            else:
                print(f"[DEBUG] No active connection for {ip}")


        if os.name == "posix":
            os.system(f'notify-send "ShotGrid Notice" "{message_text}"')

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "received_data": data}), 200

@sio.event
def connect(sid, environ):
    client_ip = environ.get("HTTP_X_FORWARDED_FOR") or environ.get("REMOTE_ADDR", "Unknown")
    connected_clients[client_ip] = sid 
    print(f"[DEBUG] Client connected: {sid} (IP: {client_ip})")

@sio.event
def disconnect(sid):
    for ip, stored_sid in list(connected_clients.items()):
        if stored_sid == sid:
            del connected_clients[ip]
            print(f"[DEBUG] Client disconnected: {ip} (SID: {sid})")
            break

def start_socketio_server():
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), flask_app)

def run_flask_in_thread():
    print("Central Server is running at other thread")
    thread = threading.Thread(target=start_socketio_server)
    thread.daemon = True
    thread.start()

def convert_ktime(utc_time_str):
    if not utc_time_str:
        return "Unknown Time"
    
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S.%f")
    utc_time = utc_time.replace(tzinfo=timezone.utc)

    kst_time = utc_time.astimezone(timezone(timedelta(hours=9)))

    return kst_time.strftime("%H:%M")

def get_assignees_ip(task_id):
    task = sg.find_one("Task", [["id", "is", task_id]], ["entity"])
    if not task or not task.get("entity"):
        print(f"Task {task_id} has no associated entity.")
        return []
    
    entity = task["entity"]
    entity_type = entity["type"]
    entity_id = entity["id"]

    filters = [["entity", "is", {"type": entity_type, "id": entity_id}]]
    fields = ["id", "content", "step", "sg_status_list", "task_assignees"]

    related_tasks = sg.find("Task", filters, fields)

    assignees_id_list = set()
    for task in related_tasks:
        task_assignees = task.get("task_assignees", [])
        for assignee in task_assignees:
            assignees_id_list.add(assignee["id"])

    if not assignees_id_list:
        print("No assignees found.")
        return []

    filters = [["id", "in", list(assignees_id_list)]]
    fields = ["id", "sg_ip"]
    users = sg.find("HumanUser", filters, fields)

    user_ip_list = []
    for user in users:
        if "sg_ip" in user:
            user_ip_list.append(f"192.168.5.{user['sg_ip']}")

    print(f"Assignee IPs: {user_ip_list}")

    return user_ip_list

print(f"{'-'*20}Central Server Running{'-'*20}")
if __name__ == "__main__":
    start_socketio_server()
else:
    run_flask_in_thread()