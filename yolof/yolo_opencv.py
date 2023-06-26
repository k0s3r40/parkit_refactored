import cv2
import argparse
import numpy as np
import json

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help='path to input image')
ap.add_argument('-c', '--config', required=True,
                help='path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help='path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help='path to text file containing class names')
args = ap.parse_args()


def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def get_detected_objects(image_path, config_path, weights_path, classes_path):
    image = cv2.imread(image_path)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open(classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    net = cv2.dnn.readNet(weights_path, config_path)

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

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

    return json.dumps(detected_objects)


# Call the get_detected_objects function to obtain the detected objects as JSON
detected_objects_json = get_detected_objects(args.image, args.config, args.weights, args.classes)
print(detected_objects_json)
