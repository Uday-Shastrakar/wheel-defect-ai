import cv2
import os
from ultralytics import YOLO
from pathlib import Path
import argparse
import time

class WheelDefectDetector:
    
    def __init__(self, model_path="models/yolov8n.pt"):
        print("🤖 Loading YOLOv8 model...")
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        print(f"✅ Model loaded successfully!")
        print(f"📋 Available classes: {self.class_names}")
    
    def detect_defects(self, image_path, confidence=0.5, save_output=True):
        print(f"🔍 Processing image: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"❌ Error: Image not found - {image_path}")
            return None, None
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Error: Could not read image - {image_path}")
            return None, None
        
        height, width = image.shape[:2]
        print(f"📏 Image size: {width}x{height}")
        
        start_time = time.time()
        results = self.model(image, conf=confidence)
        detection_time = time.time() - start_time
        
        detection_info = {
            'total_detections': 0,
            'defects': [],
            'detection_time': detection_time
        }
        
        annotated_image = image.copy()
        
        for result in results:
            boxes = result.boxes
            detection_info['total_detections'] = len(boxes)
            
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                conf = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                class_name = self.class_names[class_id]
                
                defect_info = {
                    'class': class_name,
                    'confidence': conf,
                    'bbox': [x1, y1, x2, y2]
                }
                detection_info['defects'].append(defect_info)
                
                color = (0, 255, 0) if conf > 0.7 else (0, 165, 255)
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                
                label = f"{class_name}: {conf:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(annotated_image, (x1, y1 - label_size[1] - 10), 
                            (x1 + label_size[0], y1), color, -1)
                
                cv2.putText(annotated_image, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        summary_text = f"Defects Found: {detection_info['total_detections']} | Time: {detection_time:.3f}s"
        cv2.putText(annotated_image, summary_text, (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if save_output:
            output_path = f"outputs/detected_{Path(image_path).stem}.jpg"
            cv2.imwrite(output_path, annotated_image)
            print(f"💾 Output saved: {output_path}")
        
        return annotated_image, detection_info
    
    def print_detection_summary(self, detection_info):
        print("\n" + "="*50)
        print("🔍 DETECTION RESULTS SUMMARY")
        print("="*50)
        print(f"⏱️  Detection Time: {detection_info['detection_time']:.3f} seconds")
        print(f"🔢 Total Defects Found: {detection_info['total_detections']}")
        
        if detection_info['defects']:
            print("\n📋 Defect Details:")
            for i, defect in enumerate(detection_info['defects'], 1):
                print(f"   {i}. {defect['class']} - Confidence: {defect['confidence']:.2f}")
                print(f"      Location: [{defect['bbox'][0]}, {defect['bbox'][1]}, {defect['bbox'][2]}, {defect['bbox'][3]}]")
        else:
            print("✅ No defects detected!")
        
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Detect wheel defects in images")
    parser.add_argument("--image", "-i", required=True, help="Path to input image")
    parser.add_argument("--model", "-m", default="models/yolov8n.pt", help="Path to YOLOv8 model")
    parser.add_argument("--confidence", "-c", type=float, default=0.5, help="Confidence threshold")
    parser.add_argument("--no-save", action="store_true", help="Don't save output image")
    
    args = parser.parse_args()
    
    detector = WheelDefectDetector(args.model)
    
    annotated_image, detection_info = detector.detect_defects(
        args.image, 
        args.confidence, 
        save_output=not args.no_save
    )
    
    if annotated_image is not None:
        detector.print_detection_summary(detection_info)
        
        cv2.imshow("🔍 Wheel Defect Detection Result", annotated_image)
        print("\n👀 Press any key to close the image window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ Detection failed!")

if __name__ == "__main__":
    main()
