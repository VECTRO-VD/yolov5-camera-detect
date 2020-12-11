import json
import cv2


class Area:
    filename = 'config.json'

    def __init__(self, unique_id, frame, title='', *args, **kwargs):
        self.id = str(unique_id)
        self.frame = frame
        self.x_frame = frame.shape[0]
        self.y_frame = frame.shape[1]
        self.title = title

        with open(self.filename, 'r+') as json_file:
            data = json.load(json_file)
            if self.id not in data:
                data[f'{self.id}'] = {'tops': []}
                json_file.seek(0)
                json.dump(data, json_file, indent=4)

    def create_me(self, event, x, y, img):
        with open(self.filename, 'r+') as json_file:
            data = json.load(json_file)
            tops = data[self.id]['tops']
            if event == cv2.EVENT_LBUTTONDOWN:
                if not tops:
                    cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
                else:
                    cv2.line(img, (int(tops[-1][0] * self.x_frame), int(tops[-1][1] * self.y_frame)), (x, y),
                             (0, 0, 255), 2)
                tops.append((x / self.x_frame, y / self.y_frame))
            elif event == cv2.EVENT_RBUTTONDOWN:
                cv2.line(img, (int(tops[-1][0] * self.x_frame), int(tops[-1][1] * self.y_frame)),
                         (int(tops[0][0] * self.x_frame), int(tops[0][1] * self.y_frame)), (0, 0, 255), 2)
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
