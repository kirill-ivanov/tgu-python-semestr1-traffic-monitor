import cv2
import numpy as np

from config import *
from db.dao import add_stat_all


def apply_yolo_object_detection(image_to_process):
    """
    Recognition and determination of the coordinates of objects on the image
    :param image_to_process: original image
    :return: image with marked objects and captions to them
    """

    height, width, _ = image_to_process.shape
    blob = cv2.dnn.blobFromImage(image_to_process, 1 / 255, (608, 608),
                                 (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(out_layers)
    class_indexes, class_scores, boxes = ([] for i in range(3))
    objects_count = 0

    object_result = {"car": 0, "bus": 0}
    # Starting a search for objects in an image
    for out in outs:
        for obj in out:
            scores = obj[5:]
            class_index = np.argmax(scores)
            class_score = scores[class_index]
            if class_score > 0:
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                obj_width = int(obj[2] * width)
                obj_height = int(obj[3] * height)
                box = [center_x - obj_width // 2, center_y - obj_height // 2,
                       obj_width, obj_height]
                boxes.append(box)
                class_indexes.append(class_index)
                class_scores.append(float(class_score))

    # Selection
    chosen_boxes = cv2.dnn.NMSBoxes(boxes, class_scores, 0.0, 0.4)
    for box_index in chosen_boxes:
        box_index = box_index
        box = boxes[box_index]
        class_index = class_indexes[box_index]

        # For debugging, we draw objects included in the desired classes
        if classes[class_index] in classes_to_look_for:
            object_result[classes[class_index]] = object_result[classes[class_index]] + 1
            image_to_process = draw_object_bounding_box(image_to_process,
                                                        class_index, box)

    return image_to_process, object_result


def draw_object_bounding_box(image_to_process, index, box):
    """
    Drawing object borders with captions
    :param image_to_process: original image
    :param index: index of object class defined with YOLO
    :param box: coordinates of the area around the object
    :return: image with marked objects
    """

    x, y, w, h = box
    start = (x, y)
    end = (x + w, y + h)
    color = (0, 255, 0)
    width = 2
    final_image = cv2.rectangle(image_to_process, start, end, color, width)

    start = (x, y - 10)
    font_size = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = 2
    text = classes[index]
    final_image = cv2.putText(final_image, text, start, font,
                              font_size, color, width, cv2.LINE_AA)

    return final_image


def start_video_object_detection(video: str):
    """
    Real-time video capture and analysis
    """
    while True:
        try:
            # Вытаскиваем картинку из видео
            cap = cv2.VideoCapture(video)
            i = 0
            while cap.isOpened():
                i += 1
                ret, frame = cap.read()
                if not ret:
                    break

                # Application of object recognition methods on a video frame from YOLO
                frame, stat_parsing = apply_yolo_object_detection(frame)

                if i % ALG_PERIODIC_FRAME == 0:
                    cv2.imwrite(ALG_RESULT_PHOTO_PATH, frame)
                    add_stat_all(stat_parsing)

            cap.release()
            cv2.destroyAllWindows()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':

    # Загружаем YOLO из файлов
    net = cv2.dnn.readNetFromDarknet(YOLO_PATH + "/yolov4-tiny.cfg",
                                     YOLO_PATH + "/yolov4-tiny.weights")
    layer_names = net.getLayerNames()
    out_layers_indexes = net.getUnconnectedOutLayers()
    out_layers = [layer_names[index - 1] for index in out_layers_indexes]

    # Загружаем файл с объектами YOLO, которые можно детектировать
    with open(YOLO_PATH + "/coco.names.txt") as file:
        classes = file.read().split("\n")

    list_look_for = []
    for look in YOLO_CLASS_DETECTED:
        list_look_for.append(look.strip())

    classes_to_look_for = list_look_for

    start_video_object_detection(VIDEO_URL)
