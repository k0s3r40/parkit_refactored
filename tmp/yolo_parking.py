import cv2
import argparse
import numpy as np
import json


def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers



def get_detected_objects(frame,
                         config_path='/home/slavov/PycharmProjects/parkit_refactored/yolo/yolo3.cfg',
                         weights_path='/home/slavov/PycharmProjects/parkit_refactored/yolo/object-detection-opencv/yolov3.weights',
                         classes_path='/home/slavov/PycharmProjects/parkit_refactored/yolo/yolov3.txt'):
    Width = frame.shape[1]
    Height = frame.shape[0]
    scale = 0.00392

    classes = None

    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNet(weights_path, config_path)

    blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    detected_objects = []
    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]

        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        label = classes[class_ids[i]]
        confidence = confidences[i]

        detected_objects.append({
            'label': label,
            'confidence': confidence,
            'x': round(x),
            'y': round(y),
            'width': round(w),
            'height': round(h)
        })
    print(json.dumps(detected_objects))
    return json.dumps(detected_objects)