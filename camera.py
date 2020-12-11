import uuid

import cv2

from areas import Area

uid = uuid.uuid4()


def create_area(event, x, y, flags, frame):
    global uid

    if event == cv2.EVENT_LBUTTONDOWN:
        area = Area(unique_id=uid, frame=frame)
        area.create_me(event, x, y, frame)

    elif event == cv2.EVENT_RBUTTONDOWN:
        area = Area(unique_id=uid, frame=frame)
        area.create_me(event, x, y, frame)
        uid = uuid.uuid4()
