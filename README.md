# Self-Driving Car

A behavioral-cloning project that trains a convolutional neural network to predict steering angles from camera images captured by the Udacity Self-Driving Car Simulator. A Python server loads the trained model and returns steering and throttle commands to the simulator over Socket.IO.

> **Safety:** This project is for simulation and educational use only. It is not designed or validated for controlling a real vehicle.

## Features

- Predicts steering angles from the simulator's front-facing camera.
- Preprocesses camera frames before inference.
- Adjusts throttle based on the reported vehicle speed.
- Includes Jupyter notebooks for model development and training.

## Project structure

```text
.
├── drive.py                     # Socket.IO server and real-time inference
├── model/
│   └── model.h5                 # Model loaded by drive.py
├── outputs/                     # Generated model artifacts
├── track/                       # Local simulator/training data
├── Self_drive.ipynb             # Training notebook
├── Self_Driving_Car_Fixed.ipynb # Updated/fixed notebook
└── requirements.txt             # Python dependencies
```

## Requirements

- Windows
- Python 3.10
- Udacity Self-Driving Car Simulator
- For native Windows GPU acceleration: an NVIDIA GPU, CUDA Toolkit 11.2, and cuDNN 8.1

TensorFlow 2.10.x is the final TensorFlow release with native Windows GPU support. CPU inference does not require CUDA or cuDNN.

## Setup

Open PowerShell in the project directory and create a virtual environment:

```powershell
py -3.10 -m venv .venv10
.\.venv10\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell does not allow activation, use Command Prompt instead:

```bat
.venv10\Scripts\activate.bat
```

The dependency versions are defined in [`requirements.txt`](requirements.txt). For native Windows GPU support, install the CUDA and cuDNN versions listed above and make their runtime DLLs available on `PATH`. Otherwise, TensorFlow can run on the CPU.

## Run the simulator server

1. Make sure the trained model exists at `model/model.h5`. This is the path loaded by `drive.py`.
2. Activate the virtual environment and start the server:

   ```powershell
   python drive.py
   ```

3. Start the Udacity Self-Driving Car Simulator, select a track, and enable autonomous mode. The simulator should connect to the server on port `4567`.

The server binds to `0.0.0.0:4567` so the simulator can reach it. Keep the port accessible only to trusted local applications and networks.

## Train or update the model

Open either notebook in Jupyter:

```powershell
python -m jupyter notebook
```

Run the notebook cells to follow the data preparation and training workflow. Save or copy the resulting model to `model/model.h5` before starting `drive.py`.

## Inference pipeline

For each telemetry message, `drive.py`:

1. Decodes the camera image and crops the frame to remove parts of the sky and vehicle hood.
2. Converts the image to YUV, applies a Gaussian blur, resizes it to 200 × 66 pixels, and scales pixel values.
3. Uses the loaded Keras model to predict a steering angle.
4. Calculates throttle from the reported speed and a speed limit of 10.
5. Sends the steering and throttle values back to the simulator.

## Notes

- `track/` and `outputs/` are intended for local data and generated artifacts and are excluded from Git.
- `model/model.h5` is not excluded; keep the inference model available when deploying or running the server.
- Do not commit private credentials or simulator data you do not have permission to share.
