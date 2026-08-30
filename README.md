# Remote_Vision: Real-Time Streaming Edge Vision

A high-performance, decoupled remote computer vision pipeline designed for real-time edge processing and low-latency network broadcasting.   

The system captures video streams via V4L2, executes hardware-accelerated **Ultralytics YOLO11** object detection with CUDA FP16 quantization, burn-in FPS telemetry, and packages/broadcasts the annotated stream over custom **GStreamer RTP/UDP** pipelines to a lightweight, decoupled client playback node.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%20FP16-ee4c2c?logo=pytorch)
![YOLO11](https://img.shields.io/badge/YOLO-v11m-00FFFF)
![OpenCV](https://img.shields.io/badge/OpenCV-GStreamer%20Backend-5C3EE8?logo=opencv)
![GStreamer](https://img.shields.io/badge/GStreamer-RTP%2FUDP-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#donate)
- [License](#license)

## Features

- Direct captrure from the main native camera (Cam0).
- Inference with Yolo v11.
- Send over UDP port 5000 for Playback live stream.

### Tech Stack

| Command | Description |
| --- | --- |
| Language | Python 3.12 |
| Computer Vision | OpenCV (compiled with **GStreamer & GTK backends**) |
| Deep Learning | PyTorch, Ultralytics YOLO v11 (yolo11m) |
| Streaming Framework | GStreamer 1.0 (RTP/JPEG over UDP) |
| Target OS | Linux (Ubuntu / Debian environment) |

## Installation

```bash
git clone https://github.com/PAPA/remote_vision:-real-time-edge-vision-&-streaming-pipeline.git
cd remote_vision:-real-time-edge-vision-&-streaming-pipeline
```

## Usage

Activate the Virtual Environtment (.venv)
```bash
Source .venv/bin/Activate
```

Run the Capture program
```bash
python3 Capture.py
```

Run the Playback program
```bash
python3 Playback.py
```


## Donate

If you find this project useful for your work or research, consider supporting its ongoing development!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/hilmanlajuardhie)

*Every coffee or donation helps keep experimental hardware and vision projects going. Thank you!*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤ by [PAPA](https://github.com/hilmanlajuardhie)