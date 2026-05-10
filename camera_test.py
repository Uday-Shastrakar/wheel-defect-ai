import cv2
import time

def test_camera():
    print("🎥 Starting Camera Test...")
    print("Press 'q' to quit, 's' to save snapshot")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"📹 Camera Properties:")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    
    snapshot_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error: Can't receive frame. Exiting...")
            break
        
        cv2.putText(frame, "Press 'q' to quit, 's' to save snapshot", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow("🔍 Wheel Camera Test - Press 'q' to exit", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("👋 Camera test ended by user")
            break
        
        elif key == ord('s'):
            snapshot_count += 1
            filename = f"images/snapshot_{snapshot_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Snapshot saved: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Camera test completed")

if __name__ == "__main__":
    test_camera()