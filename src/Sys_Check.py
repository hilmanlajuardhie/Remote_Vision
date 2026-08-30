import sys
import subprocess
import importlib
import re

# ANSI colors for terminal formatting
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_status(status, message):
    if status == "OK":
        print(f"[{GREEN} OK {RESET}] {message}")
    elif status == "FAIL":
        print(f"[{RED}FAIL{RESET}] {message}")
    elif status == "WARN":
        print(f"[{YELLOW}WARN{RESET}] {message}")

def check_all_dependencies():
    print("========================================")
    print("   Streaming Project Dependency Check   ")
    print("========================================\n")

    # 1. Check Python Packages
    print("--- 1. Python Packages ---")
    packages = {
        "cv2": "OpenCV",
        "torch": "PyTorch",
        "numpy": "NumPy",
        "ultralytics": "Ultralytics (YOLO)"
    }
    
    has_cv2 = False
    for module, name in packages.items():
        try:
            importlib.import_module(module)
            print_status("OK", f"{name} is installed.")
            if module == "cv2":
                has_cv2 = True
        except ImportError:
            print_status("FAIL", f"{name} is missing! (Run: pip install {module})")
    
    # 2. Check OpenCV Build (GStreamer & GTK)
    print("\n--- 2. OpenCV Build Configuration ---")
    if has_cv2:
        import cv2
        info = cv2.getBuildInformation()
        
        # Check GStreamer
        if re.search(r'GStreamer:\s*YES', info):
            print_status("OK", "OpenCV GStreamer support is ENABLED.")
        else:
            print_status("FAIL", "OpenCV GStreamer support is MISSING. (VideoWriter will fail)")
            
        # Check GTK (GUI)
        if re.search(r'GTK.?:\s*YES', info, re.IGNORECASE):
            print_status("OK", "OpenCV GTK (Window) support is ENABLED.")
        else:
            print_status("FAIL", "OpenCV GTK support is MISSING. (cv.imshow will crash)")
    else:
        print_status("FAIL", "Skipping OpenCV build check because cv2 is not installed.")

    # 3. Check PyTorch CUDA Acceleration
    print("\n--- 3. Hardware Acceleration ---")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print_status("OK", f"PyTorch CUDA is enabled! Detected GPU: {gpu_name}")
        else:
            print_status("WARN", "PyTorch CUDA is NOT available. YOLO inference will run on CPU.")
    except ImportError:
        print_status("FAIL", "Skipping CUDA check because PyTorch is not installed.")

    # 4. Check System GStreamer
    print("\n--- 4. System GStreamer Tools ---")
    try:
        subprocess.run(["gst-launch-1.0", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print_status("OK", "Ubuntu GStreamer CLI tools are installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("FAIL", "System GStreamer tools are missing! (Run: sudo apt-get install gstreamer1.0-tools)")
        
    print("\n========================================")
    print("Diagnosis Complete.")

if __name__ == "__main__":
    check_all_dependencies()