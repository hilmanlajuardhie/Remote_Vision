# Remote_Vision: Real-Time Edge Vision & Streaming Pipeline

A high-performance, decoupled remote computer vision pipeline designed for real-time edge processing and low-latency network broadcasting.   

The system captures video streams via V4L2, executes hardware-accelerated **Ultralytics YOLO11** object detection with CUDA FP16 quantization, burn-in FPS telemetry, and packages/broadcasts the annotated stream over custom **GStreamer RTP/UDP** pipelines to a lightweight, decoupled client playback node.

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Feature 1
- Feature 2
- Feature 3

### Tech Stack

- **Python**
- **OpenCV**
- **GStreamer**
- **Yolo v11**

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

Describe how to use the project here.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤ by [PAPA](https://github.com/hilmanlajuardhie)