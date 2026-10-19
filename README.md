🚗 Complete Self-Driving Car (Behavioral Cloning)

This project trains a deep neural network to drive a car autonomously on a virtual track using the Udacity Self-Driving Car Simulator. It uses Behavioral Cloning, where the model learns to clone human driving behavior by mapping front-facing camera images to steering angles.

🛠️ Tech Stack & Requirements

This project relies on a very specific environment stack to enable Native Windows GPU Acceleration using an NVIDIA GPU (e.g., RTX 4050).

Python: 3.10.11 (Strictly required for Windows Native GPU support)

TensorFlow / Keras: 2.10.0 (Last version to support Native Windows GPU)

CUDA Toolkit: 11.2

cuDNN: 8.1.1

Simulator: Udacity Self-Driving Car Simulator

📦 Installation & Setup

1. Create the Environment

You must use Python 3.10. Create and activate your virtual environment:

py -3.10 -m venv .venv10
.\.venv10\Scripts\Activate.ps1


2. Install Dependencies

Due to version conflicts with the older Udacity simulator and TensorFlow 2.10, run these exact commands to install the perfectly balanced stack:

# Install legacy GPU-enabled TensorFlow and compatible NumPy
pip install tensorflow-gpu==2.10.0 keras==2.10.0 "numpy<2" protobuf==3.19.6

# Install compatible OpenCV and data tools
pip install "opencv-python<5" "opencv-contrib-python<5" "ml-dtypes<0.4" pandas matplotlib imgaug

# Install legacy Socket.IO required to communicate with the Udacity Simulator
pip install python-socketio==4.6.1 python-engineio==3.13.2 Flask eventlet Pillow


3. GPU Configuration (Windows Native)

If TensorFlow fails to detect your GPU or throws cudnn DLL errors:

Download CUDA Toolkit 11.2.2 and install it.

Download cuDNN v8.1.1.

Extract the cuDNN .zip file, open the bin folder, and copy all the .dll files.

Paste these .dll files directly into your virtual environment's script folder: .venv10\Scripts\.

🚀 Usage

1. Start the AI Server

Activate your environment and run the driving script:

python drive.py


You should see wsgi starting up on http://0.0.0.0:4567 in your terminal.

2. Launch the Simulator

Open the Udacity Self-Driving Car Simulator executable.

Select your graphics settings and track.

Click on Autonomous Mode.

The simulator will connect to the drive.py server. Your terminal will print the telemetry data (steering angle, throttle, speed), and the car will begin driving itself!

📁 Project Structure

drive.py: The Flask server that handles the Socket.IO connection to the simulator. It loads the trained model, preprocesses incoming camera frames, predicts the steering angle, and sends throttle/steering commands back to the car.

model.h5: The compiled and trained Keras neural network model.

Self_Driving_Car.ipynb: The Jupyter Notebook used to build, compile, and train the Convolutional Neural Network (CNN).

🧠 How It Works

Image Preprocessing: Images from the simulator's center camera are cropped (to remove the sky and car hood), converted to YUV color space, blurred to reduce noise, and normalized.

Prediction: The preprocessed image is fed into the loaded Keras model (model.h5).

Control: The model outputs a continuous value for the steering angle. The throttle is dynamically calculated based on the current speed, and both values are emitted back to the simulator via WebSockets.