import socket
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv

# 1. Initialize UDP Socket transmitter for real-time data streaming to Unity
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Load the lightweight pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# 3. Initialize the webcam feed
cap = cv2.VideoCapture(0)

# 4. Define the polygon vertices for the mall's high-traffic hotspot zone
# This sets up a 300x300 pixel tracking zone in the center of the camera frame
polygon = np.array([[100, 100], [400, 100], [400, 400], [100, 400]])

# 5. Initialize Roboflow Supervision's PolygonZone and Annotators
zone = sv.PolygonZone(polygon=polygon)
zone_annotator = sv.PolygonZoneAnnotator(
    zone=zone, color=sv.Color.from_hex("#ff00ff"), thickness=4
)
box_annotator = sv.BoxAnnotator()

print("Mall Advanced AI Traffic Analytics System Active.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Execute real-time object detection inference via YOLOv8
    results = model(frame, stream=True)

    for r in results:
        # Convert Ultralytics inference results into Supervision compatible format
        detections = sv.Detections.from_ultralytics(r)

        # Explicitly filter detections to only track 'person' (class_id == 0)
        detections = detections[detections.class_id == 0]

        # Trigger zone evaluation to verify if targets entered the polygon perimeter
        zone.trigger(detections=detections)

        # Render object tracking bounding boxes onto the frame
        frame = box_annotator.annotate(scene=frame, detections=detections)

    # Render the virtual polygon zone and live head-count metrics on the UI display
    frame = zone_annotator.annotate(scene=frame)

    # 🚀 Broadcast the current zone occupancy count directly to Unity via UDP
    crowd_count = zone.current_count
    data_string = f"mall_crowd:{crowd_count}"
    sock.sendto(data_string.encode("utf-8"), (UDP_IP, UDP_PORT))

    # Display the refined Edge AI analytics video stream
    cv2.imshow("Mall Crowd Analytics System (Supervision PoC)", frame)

    # Terminate video stream execution if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Safely release camera hardware resources and destroy UI windows
cap.release()
cv2.destroyAllWindows()
