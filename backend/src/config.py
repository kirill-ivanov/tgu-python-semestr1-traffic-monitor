import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))



YOLO_PATH = ROOT_PATH + "/resources/yolo"
YOLO_CLASS_DETECTED = ["car", "bus"]

VIDEO_URL = ROOT_PATH + "/resources/video/video_3.mp4"

ALG_PERIODIC_FRAME = 10
ALG_RESULT_PHOTO_PATH = ROOT_PATH + "/web/public/result/out_result.jpg"

DB_PATH = ROOT_PATH + "/traffic_db.db"
