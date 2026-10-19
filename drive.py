
import socketio
import eventlet
import numpy as np
from flask import Flask
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2

sio = socketio.Server()
app = Flask(__name__)

speed_limit = 10.0


def img_preprocess(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255.0
    return img


def send_control(steering_angle, throttle, sid=None):
    control_data = {
        "steering_angle": str(float(steering_angle)),
        "throttle": str(float(throttle))
    }

    # Send to the connected simulator client.
    sio.emit("steer", data=control_data, to=sid)


@sio.on("connect")
def connect(sid, environ, auth=None):
    print(f"Simulator connected: {sid}")
    send_control(0.0, 0.0, sid)


@sio.on("telemetry")
def telemetry(sid, data):
    try:
        if not data or "speed" not in data or "image" not in data:
            print("Invalid telemetry received")
            return

        speed = float(data["speed"])

        raw_image = Image.open(
            BytesIO(base64.b64decode(data["image"]))
        ).convert("RGB")

        image = np.asarray(raw_image)
        image = img_preprocess(image)
        image = np.expand_dims(image, axis=0)

        prediction = model.predict(image, verbose=0)
        steering_angle = float(np.asarray(prediction).reshape(-1)[0])

        throttle = max(0.0, min(1.0, 1.0 - speed / speed_limit))

        print(
            f"Speed: {speed:.2f} | "
            f"Steering: {steering_angle:.4f} | "
            f"Throttle: {throttle:.3f}"
        )

        send_control(steering_angle, throttle, sid)

    except Exception as exc:
        print(f"Telemetry error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    model = load_model(
        r"./model/model.h5",
        compile=False
    )

    print("Model loaded successfully")
    print("Waiting for simulator on port 4567...")

    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 4567)), app)
