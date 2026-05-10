import os
import sys
import subprocess
import venv
from pathlib import Path

def check_python_version():
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True

def create_virtual_environment():
    venv_path = Path("wheel_defect_env")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def get_venv_python():
    if os.name == 'nt':
        return Path("wheel_defect_env/Scripts/python.exe")
    else:
        return Path("wheel_defect_env/bin/python")

def get_venv_pip():
    if os.name == 'nt':
        return Path("wheel_defect_env/Scripts/pip.exe")
    else:
        return Path("wheel_defect_env/bin/pip")

def install_dependencies():
    print("📚 Installing dependencies...")
    
    pip_path = get_venv_pip()
    requirements_path = Path("requirements.txt")
    
    if not requirements_path.exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        print("   Upgrading pip...")
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        print("   Installing packages from requirements.txt...")
        subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], 
                      check=True, capture_output=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    print("📁 Creating directories...")
    
    directories = ["dataset", "images", "outputs", "models"]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"   Created: {directory}")
        else:
            print(f"   Exists: {directory}")

def download_yolo_model():
    print("🤖 Downloading YOLOv8 model...")
    
    python_path = get_venv_python()
    models_path = Path("models")
    models_path.mkdir(exist_ok=True)
    
    try:
        result = subprocess.run([
            str(python_path), "-c", 
            "from ultralytics import YOLO; YOLO('yolov8n.pt'); print('Model downloaded successfully')"
        ], check=True, capture_output=True, text=True)
        
        model_files = list(Path(".").glob("yolov8n.pt"))
        if model_files:
            import shutil
            shutil.move(str(model_files[0]), "models/yolov8n.pt")
            print("✅ YOLOv8n model downloaded to models/")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading model: {e}")
        print("   Model will be downloaded automatically on first run")
        return False

def print_setup_complete():
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Activate virtual environment:")
    
    if os.name == 'nt':
        print("   wheel_defect_env\\Scripts\\activate")
    else:
        print("   source wheel_defect_env/bin/activate")
    
    print("\n2. Test your camera:")
    print("   python camera_test.py")
    
    print("\n3. Run detection:")
    print("   python detect.py --image your_image.jpg")
    print("   python realtime_detect.py")
    
    print("\n4. For training custom model:")
    print("   - Prepare dataset in dataset/ folder")
    print("   - Check README.md for training instructions")
    
    print("\n📚 More information:")
    print("   - Read README.md for detailed instructions")
    print("   - Check each script for inline comments")
    
    print("\n" + "="*60)

def main():
    print("🔧 Alloy Wheel Defect Detection System Setup")
    print("="*60)
    
    if not check_python_version():
        return
    
    if not create_virtual_environment():
        return
    
    if not install_dependencies():
        return
    
    create_directories()
    
    download_yolo_model()
    
    print_setup_complete()

if __name__ == "__main__":
    main()
