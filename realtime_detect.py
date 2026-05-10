import cv2
import os
import time
from ultralytics import YOLO
from pathlib import Path
import argparse
from datetime import datetime

class RealTimeWheelDefectDetector:
    
    def __init__(self, model_path="models/yolov8n.pt", camera_index=0):
        print("🤖 Loading YOLOv8 model...")
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        self.camera_index = camera_index
        
        self.cap = cv2.VideoCapture(camera_index)
        
        if not self.cap.isOpened():
            print(f"❌ Error: Could not open camera {camera_index}")
            raise Exception(f"Camera {camera_index} not found")
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        print(f"✅ Model loaded successfully!")
        print(f"📹 Camera initialized: {self.width}x{self.height} @ {self.fps} FPS")
        print(f"📋 Available classes: {self.class_names}")
        
        self.frame_count = 0
        self.total_detections = 0
        self.start_time = time.time()
    
    def process_frame(self, frame, confidence=0.5):
        start_time = time.time()
        results = self.model(frame, conf=confidence)
        detection_time = time.time() - start_time
        
        detection_info = {
            'frame_detections': 0,
            'defects': [],
            'detection_time': detection_time
        }
        
        annotated_frame = frame.copy()
        
        for result in results:
            boxes = result.boxes
            detection_info['frame_detections'] = len(boxes)
            
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
                
                if conf > 0.8:
                    color = (0, 255, 0)
                elif conf > 0.6:
                    color = (0, 165, 255)
                else:
                    color = (0, 0, 255)
                
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                
                label = f"{class_name}: {conf:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                            (x1 + label_size[0], y1), color, -1)
                
                cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return annotated_frame, detection_info
    
    def add_info_overlay(self, frame, detection_info):
        overlay_frame = frame.copy()
        
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
        
        overlay_texts = [
            f"🔍 Wheel Defect Detection",
            f"📹 FPS: {fps:.1f}",
            f"⏱️  Detection Time: {detection_info['detection_time']:.3f}s",
            f"🔢 Frame Defects: {detection_info['frame_detections']}",
            f"📊 Total Detections: {self.total_detections}",
            f"🎯 Confidence: {detection_info.get('confidence', 0.5):.2f}"
        ]
        
        overlay_height = len(overlay_texts) * 25 + 20
        cv2.rectangle(overlay_frame, (10, 10), (350, overlay_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay_frame, 0.7, frame, 0.3, 0, overlay_frame)
        
        y_offset = 30
        for text in overlay_texts:
            cv2.putText(overlay_frame, text, (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 25
        
        instructions = [
            "Press 'q' to quit",
            "Press 's' to save snapshot",
            "Press 'c' to clear statistics"
        ]
        
        y_offset = self.height - 80
        for instruction in instructions:
            cv2.putText(overlay_frame, instruction, (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            y_offset += 25
        
        return overlay_frame
    
    def save_snapshot(self, frame, detection_info):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/realtime_snapshot_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        
        print(f"📸 Snapshot saved: {filename}")
        print(f"   Defects in frame: {detection_info['frame_detections']}")
    
    def run_detection(self, confidence=0.5, save_video=False):
        print("\n🎥 Starting Real-time Detection...")
        print("📋 Controls:")
        print("   'q' - Quit")
        print("   's' - Save snapshot")
        print("   'c' - Clear statistics")
        
        video_writer = None
        if save_video:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = f"outputs/realtime_detection_{timestamp}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (self.width, self.height))
            print(f"🎥 Recording video to: {video_path}")
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("❌ Error: Can't receive frame. Exiting...")
                    break
                
                annotated_frame, detection_info = self.process_frame(frame, confidence)
                detection_info['confidence'] = confidence
                
                self.frame_count += 1
                self.total_detections += detection_info['frame_detections']
                
                final_frame = self.add_info_overlay(annotated_frame, detection_info)
                
                cv2.imshow("🔍 Real-time Wheel Defect Detection", final_frame)
                
                if save_video and video_writer is not None:
                    video_writer.write(final_frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("👋 Real-time detection ended by user")
                    break
                
                elif key == ord('s'):
                    self.save_snapshot(final_frame, detection_info)
                
                elif key == ord('c'):
                    self.frame_count = 0
                    self.total_detections = 0
                    self.start_time = time.time()
                    print("📊 Statistics cleared")
        
        finally:
            if video_writer is not None:
                video_writer.release()
                print(f"✅ Video saved successfully")
            
            self.cap.release()
            cv2.destroyAllWindows()
            
            self.print_final_statistics()
    
    def print_final_statistics(self):
        total_time = time.time() - self.start_time
        avg_fps = self.frame_count / total_time if total_time > 0 else 0
        
        print("\n" + "="*50)
        print("📊 FINAL DETECTION STATISTICS")
        print("="*50)
        print(f"⏱️  Total Runtime: {total_time:.2f} seconds")
        print(f"🎬 Frames Processed: {self.frame_count}")
        print(f"📹 Average FPS: {avg_fps:.2f}")
        print(f"🔢 Total Detections: {self.total_detections}")
        print(f"📈 Detection Rate: {self.total_detections/self.frame_count:.2f} defects/frame" if self.frame_count > 0 else "📈 Detection Rate: N/A")
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Real-time wheel defect detection")
    parser.add_argument("--model", "-m", default="models/yolov8n.pt", help="Path to YOLOv8 model")
    parser.add_argument("--camera", "-c", type=int, default=0, help="Camera index")
    parser.add_argument("--confidence", type=float, default=0.5, help="Confidence threshold")
    parser.add_argument("--save-video", action="store_true", help="Save detection video")
    
    args = parser.parse_args()
    
    try:
        detector = RealTimeWheelDefectDetector(args.model, args.camera)
        
        detector.run_detection(args.confidence, args.save_video)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your camera connection and model path.")

if __name__ == "__main__":
    main()
