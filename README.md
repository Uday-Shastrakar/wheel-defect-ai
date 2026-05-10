# 🔍 Alloy Wheel Defect Detection System

An AI-powered system for detecting defects in alloy wheels using YOLOv8, OpenCV, and Python. This project is designed for beginners and provides a clean, modular structure for wheel defect detection.

## 🎯 Project Features

- **Real-time Detection**: Live webcam detection with confidence scores
- **Image Detection**: Process individual wheel images
- **Multiple Defect Types**: Detect scratches, dents, bumps, and paint damage
- **Visual Feedback**: Bounding boxes with confidence percentages
- **Output Saving**: Save detected images and videos
- **Beginner Friendly**: Clean code with detailed comments
- **Modular Design**: Easy to extend for robotics integration

## 📁 Project Structure

```
wheel-defect-ai/
│
├── dataset/              # Training dataset (images + labels)
│   ├── images/          # Training images
│   └── labels/          # YOLO format labels
│
├── images/              # Test images and snapshots
├── outputs/             # Detection results (images + videos)
├── models/              # Trained YOLOv8 models
│
├── camera_test.py       # Webcam testing script
├── detect.py            # Image detection script
├── realtime_detect.py   # Real-time webcam detection
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv wheel_defect_env

# Activate on Windows
wheel_defect_env\Scripts\activate

# Activate on Linux/Mac
source wheel_defect_env/bin/activate
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 3. Test Your Camera

```bash
# Test if your webcam is working
python camera_test.py
```

### 4. Run Detection

#### Image Detection:
```bash
# Detect defects in an image
python detect.py --image path/to/your/wheel_image.jpg

# With custom confidence threshold
python detect.py --image path/to/your/wheel_image.jpg --confidence 0.7

# Using custom model
python detect.py --image path/to/your/wheel_image.jpg --model models/custom_model.pt
```

#### Real-time Detection:
```bash
# Start real-time detection
python realtime_detect.py

# With custom settings
python realtime_detect.py --confidence 0.6 --camera 0 --save-video
```

## 📋 Available Scripts

### 1. `camera_test.py` - Camera Testing
- Tests your webcam functionality
- Displays live video feed
- Save snapshots with 's' key
- Press 'q' to quit

**Usage:**
```bash
python camera_test.py
```

### 2. `detect.py` - Image Detection
- Detects defects in static images
- Shows bounding boxes and confidence scores
- Saves annotated output images
- Provides detailed detection summary

**Usage:**
```bash
python detect.py --image path/to/image.jpg --confidence 0.5
```

**Options:**
- `--image, -i`: Path to input image (required)
- `--model, -m`: Path to YOLOv8 model (default: models/yolov8n.pt)
- `--confidence, -c`: Confidence threshold (default: 0.5)
- `--no-save`: Don't save output image

### 3. `realtime_detect.py` - Live Detection
- Real-time webcam detection
- Live statistics overlay
- Save snapshots and videos
- Interactive controls

**Usage:**
```bash
python realtime_detect.py --confidence 0.5 --camera 0 --save-video
```

**Options:**
- `--model, -m`: Path to YOLOv8 model
- `--camera, -c`: Camera index (default: 0)
- `--confidence`: Confidence threshold (default: 0.5)
- `--save-video`: Save detection video

**Controls:**
- `q`: Quit application
- `s`: Save snapshot
- `c`: Clear statistics

## 🎮 Controls Guide

### Camera Test
- **'q'**: Quit camera test
- **'s'**: Save snapshot

### Real-time Detection
- **'q'**: Quit detection
- **'s'**: Save current frame as snapshot
- **'c'**: Clear detection statistics

## 🤖 Training Your Custom Model

### 1. Prepare Dataset
Create your dataset in YOLO format:

```
dataset/
├── images/
│   ├── train/
│   │   ├── wheel1.jpg
│   │   ├── wheel2.jpg
│   │   └── ...
│   └── val/
│       ├── wheel101.jpg
│       ├── wheel102.jpg
│       └── ...
└── labels/
    ├── train/
    │   ├── wheel1.txt
    │   ├── wheel2.txt
    │   └── ...
    └── val/
        ├── wheel101.txt
        ├── wheel102.txt
        └── ...
```

### 2. Label Format
Each label file should contain lines in this format:
```
<class_id> <x_center> <y_center> <width> <height>
```

Example for a scratch defect:
```
0 0.5 0.3 0.2 0.1
```

### 3. Create Dataset Configuration
Create `dataset.yaml`:
```yaml
# Wheel Defect Dataset Configuration
path: dataset  # dataset root dir
train: images/train  # train images
val: images/val  # val images

# Classes
names:
  0: scratch
  1: dent
  2: bump
  3: paint_damage
```

### 4. Train Model
```bash
# Train custom YOLOv8 model
yolo train data=dataset.yaml model=yolov8n.pt epochs=50 imgsz=640

# Train with specific parameters
yolo train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640 batch=16
```

### 5. Validate Model
```bash
# Validate trained model
yolo val model=runs/detect/train/weights/best.pt data=dataset.yaml
```

### 6. Use Custom Model
```bash
# Use your trained model
python detect.py --image test.jpg --model runs/detect/train/weights/best.pt
python realtime_detect.py --model runs/detect/train/weights/best.pt
```

## 🔧 Configuration

### Model Options
- **YOLOv8n**: Nano version (fast, less accurate)
- **YOLOv8s**: Small version (balanced)
- **YOLOv8m**: Medium version (more accurate)
- **YOLOv8l**: Large version (very accurate)
- **YOLOv8x**: Extra large version (most accurate)

### Confidence Thresholds
- **0.8+**: High confidence (few false positives)
- **0.6-0.8**: Medium confidence (balanced)
- **0.4-0.6**: Low confidence (more detections)
- **<0.4**: Very low (may include false positives)

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Found
```bash
# Check available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).read()[0]])"
```

#### Model Loading Error
- Ensure model file exists in `models/` folder
- Check if ultralytics is installed correctly
- Verify model file is not corrupted

#### Low Detection Accuracy
- Lower confidence threshold
- Use larger model (yolov8s, yolov8m)
- Train custom model with your dataset
- Improve image quality and lighting

#### Memory Issues
- Reduce image size in training
- Use smaller batch size
- Close other applications

### Performance Tips

1. **Use GPU**: Install CUDA for faster training and inference
2. **Optimize Model**: Use YOLOv8n for real-time applications
3. **Image Resolution**: Higher resolution = better accuracy but slower
4. **Lighting**: Good lighting improves detection accuracy

## 🔮 Future Extensions

### Robotics Integration
- ROS2 node for quadruped robots
- Serial communication for robotic arms
- Integration with conveyor belt systems

### Advanced Features
- Defect severity classification
- 3D defect mapping
- Automated reporting system
- Cloud-based processing

### Mobile Deployment
- Convert to ONNX format
- Deploy on edge devices
- Mobile app development

## 📚 Dependencies

- **Python 3.8+**: Core programming language
- **OpenCV**: Computer vision and image processing
- **Ultralytics**: YOLOv8 implementation
- **PyTorch**: Deep learning framework
- **NumPy**: Numerical computing
- **Pillow**: Image processing

## 📄 License

This project is for educational and research purposes. Please ensure you have proper licenses for any commercial use.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with different parameters
4. Create an issue with detailed information

---

**Happy Coding! 🚀**

Built with ❤️ for wheel defect detection
