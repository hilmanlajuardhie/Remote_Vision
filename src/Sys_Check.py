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

def check_cv_dependencies():
    print("========================================")
    print("   Streaming Project Dependency Check   ")
    print("========================================\n")

    print("--- 1. Python Environment ---")
    py_ver = sys.version_info
    py_str = f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"
    if py_ver >= (3, 10):
        print_status("OK", f"Python version\t: {py_str}.")
    else:
        print_status("WARN", f"Python version\t: {py_str} (3.10+ recommended).")

    # 2. Check Python Packages
    print("\n--- 2. Python Packages ---")
    packages = {
        "numpy": "NumPy\t\t",
        "cv2": "OpenCV\t\t",
        "torch": "PyTorch\t\t",
        "ultralytics": "Ultralytics\t"
    }
    
    installed = {}
    for module, name in packages.items():
        try:
            mod = importlib.import_module(module)
            version = getattr(mod, "__version__", "Installed")
            print_status("OK", f"{name}: v{version}")
            installed[module] = True
        except ImportError:
            print_status("FAIL", f"{name} is missing! (pip install {module})")
            installed[module] = False
    
    # 3. Check OpenCV Build (GStreamer & GTK)
    print("\n--- 3. OpenCV Build Configuration ---")    
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
    
    # 4. Check PyTorch CUDA Acceleration
    print("\n--- 4. Hardware Acceleration ---")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print_status("OK", f"PyTorch CUDA active.\n       GPU: {gpu_name}")
        else:
            print_status("WARN", "PyTorch CUDA is NOT available. YOLO inference will run on CPU.")
    except ImportError:
        print_status("FAIL", "Skipping CUDA check because PyTorch is not installed.")

    # 5. Check System GStreamer
    print("\n--- 5. System GStreamer Tools ---")
    try:
        subprocess.run(["gst-launch-1.0", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print_status("OK", "Ubuntu GStreamer CLI tools are installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("FAIL", "System GStreamer tools are missing! (Run: sudo apt-get install gstreamer1.0-tools)")
        
    print("\n========================================")
    print("Diagnosis Complete.")

if __name__ == "__main__":
    check_cv_dependencies()