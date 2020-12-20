import uuid

import cv2

from zones import Area

uid = uuid.uuid4()


def create_area(event, x, y, flags, frame):
    global uid

    area_object = Area(unique_id=uid, frame=frame)
    if event == cv2.EVENT_LBUTTONDOWN:
        area_object.create_me(event, x, y, frame)

    elif event == cv2.EVENT_RBUTTONDOWN:
        area_object.create_me(event, x, y, frame)
        uid = uuid.uuid4()
