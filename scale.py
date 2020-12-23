import json
import numpy as np

import cv2
from shapely.geometry.polygon import Polygon, Point

from utils.mqtt import host as broker_host
import paho.mqtt.client as mqtt

check = False

broker_port = 1883

username = 'testuser'
password = 'P@ssw0rd'

client = mqtt.Client()
client.username_pw_set(username)
client.connect(broker_host, broker_port)
client.loop_start()


def add_two_images(img1, img2):
    cv2.addWeighted(img1, 0.5, img2, 0.5, 0)


def scaling(x, y, elem):
    return int(elem[0] * x), int(elem[1] * y)


def create_polygons(filename, x, y):
    with open(filename, 'r+') as json_file:
        data = json.load(json_file)

    polygons = []
    for area in data:
        tops = data[area]['tops']
        cords = []
        for top in tops:
            cords.append(scaling(x, y, top))
        polygons.append(Polygon(cords))

    return polygons


def polygons_intersection(xyxy, polygons, img):
    global check

    overlay = img.copy()

    x, y, x2, y2 = [int(i) for i in xyxy]
    person = Polygon([(x, y), (x2, y), (x2, y2), (x, y2)])
    legs_dot = (x2 - int((x2 - x) / 2), y2 + 2)
    cv2.circle(img, legs_dot, 2, (255, 0, 255), 3)

    for polygon in polygons:
        if not Point(legs_dot).within(polygon):
            if polygon.intersects(person):
                inter = polygon.intersection(person)
                if type(inter) == Polygon:
                    cords = [(int(xy[0]), int(xy[1])) for xy in list(inter.exterior.coords)]
                    if not check:
                        client.publish('lamp/system', '1')
                        check = True
                        print(check)
                    # for i in range(len(cords) - 1):  # draw intersection
                    # cv2.line(img, cords[i], cords[i + 1], (0, 255, 255), 5)
                    cv2.fillPoly(img, np.array([cords], dtype=np.int64), (255, 0, 255))
                    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        else:
            if check:
                client.publish('lamp/system', '0')
                check = False
                print(check)
