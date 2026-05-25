import cv2
import numpy as np
import base64

COLORS = {
    "INVOICE": (255, 165, 0),
    "BANK_SLIP": (0, 255, 0),
    "ID_CARD": (255, 0, 0),
    "RECEIPT": (0, 165, 255),
    "UNKNOWN": (128, 128, 128)
}

def draw_boxes(image_bytes: bytes, boxes: list, doc_type: str) -> str:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    color = COLORS.get(doc_type, (128, 128, 128))

    for box in boxes:
        x = box['x']
        y = box['y']
        w = box['width']
        h = box['height']
        text = box['text']
        conf = box['confidence']

        # Draw bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

        # Draw confidence score above box
        cv2.putText(
            img,
            f"{conf}%",
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            color,
            1
        )

    # Convert back to base64 to send to frontend
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return img_base64


def highlight_fields(image_bytes: bytes, boxes: list, parsed_fields: dict, doc_type: str) -> str:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    color = COLORS.get(doc_type, (128, 128, 128))

    # Flatten parsed field values for matching
    field_values = []
    for key, val in parsed_fields.items():
        if isinstance(val, str):
            field_values.append(val.lower())
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, str):
                    field_values.append(item.lower())
                elif isinstance(item, dict):
                    for v in item.values():
                        if isinstance(v, str):
                            field_values.append(v.lower())

    for box in boxes:
        text = box['text'].lower()
        x = box['x']
        y = box['y']
        w = box['width']
        h = box['height']

        # Highlight boxes that match parsed fields
        is_key_field = any(text in val or val in text for val in field_values)

        if is_key_field:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.rectangle(img, (x, y), (x + w, y + h), (*color, 50), -1)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), 1)

    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return img_base64