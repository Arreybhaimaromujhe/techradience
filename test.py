import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports
import time
import sys

# Force UTF-8 encoding for stdout to prevent UnicodeEncodeError on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Serial connection configuration
def get_available_ports():
    ports = serial.tools.list_ports.comports()
    bluetooth_ports = []
    other_ports = []
    
    for port in ports:
        # Check if it looks like a Bluetooth serial port based on its description in Windows
        if "Bluetooth" in port.description or "BthModem" in port.description or "Standard Serial" in port.description:
            bluetooth_ports.append(port.device)
        else:
            other_ports.append(port.device)
            
    # Prefer Bluetooth ports, but fall back to testing other ports if none are found
    return bluetooth_ports + other_ports

BLUETOOTH_PORTS = get_available_ports()
BAUD_RATE = 9600
CONNECTION_TIMEOUT = 2
RECONNECT_INTERVAL = 3

# Global Bluetooth connection object
bluetooth = None
connected = False
last_reconnect_time = 0

def initialize_bluetooth():
    """Try to connect to HC-05 on available COM ports"""
    global bluetooth, connected
    
    for port in BLUETOOTH_PORTS:
        try:
            print(f"Attempting to connect on {port}...")
            bluetooth = serial.Serial(port, BAUD_RATE, timeout=CONNECTION_TIMEOUT)
            time.sleep(1)
            
            if bluetooth.is_open:
                connected = True
                print(f"✓ Successfully connected to HC-05 on {port}")
                return True
        except serial.SerialException as e:
            print(f"✗ Failed to connect on {port}: {e}")
            if bluetooth:
                try:
                    bluetooth.close()
                except:
                    pass
        except Exception as e:
            print(f"✗ Unexpected error on {port}: {e}")
    
    print("⚠ HC-05 not found on any COM port. Continuing in demo mode...")
    connected = False
    return False

def send_command(command):
    """Safely send command to Arduino via HC-05"""
    global bluetooth, connected, last_reconnect_time
    
    if not connected:
        # Try to reconnect if enough time has passed
        if time.time() - last_reconnect_time > RECONNECT_INTERVAL:
            print("Attempting to reconnect to HC-05...")
            last_reconnect_time = time.time()
            initialize_bluetooth()
        return False
    
    try:
        if bluetooth and bluetooth.is_open:
            bluetooth.write(command.encode())
            return True
        else:
            connected = False
            return False
    except (serial.SerialException, AttributeError) as e:
        print(f"\nBluetooth write error: {e}", flush=True)
        print("!! WARNING: If it disconnected as soon as the car tried to move, your !!", flush=True)
        print("!! Arduino/Motors are drawing too much power and killing the HC-05!   !!", flush=True)
        connected = False
        last_reconnect_time = time.time()
        return False
    except Exception as e:
        print(f"Unexpected error sending command: {e}")
        return False

# Initialize Bluetooth connection
print("\n" + "="*50)
print("HAND GESTURE ROBOT CONTROL SYSTEM")
print("="*50)
initialize_bluetooth()

# Gesture-to-command mapping (same as before)
def get_command(fingers):
    if fingers == [0,1,0,0,0]: return 'F'
    elif fingers == [0,1,1,0,0]: return 'B'
    elif fingers == [0,1,0,0,1]: return 'L'
    elif fingers == [0,1,1,1,1]: return 'R'
    else: return 'S'

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam!")
    sys.exit(1)

print("\n" + "-"*50)
print("GESTURE CONTROLS:")
print("  [0,1,0,0,0] = F (Forward)")
print("  [0,1,1,0,0] = B (Backward)")
print("  [0,1,0,0,1] = L (Left)")
print("  [0,1,1,1,1] = R (Right)")
print("  Other       = S (Stop)")
print("-"*50)
print("Press 'q' to quit")
print("="*50 + "\n")

last_command = None
last_send_time = 0
frame_count = 0

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to read frame from webcam")
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    try:
        results = hands.process(img_rgb)
    except Exception as e:
        print(f"Error processing frame: {e}")
        continue

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        fingers = []

        # Thumb detection (right hand)
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Check other fingers (same as before)
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                fingers.append(1)
            else:
                fingers.append(0)

        # Send command via Bluetooth
        command = get_command(fingers)
        
        current_time = time.time()
        # Send command if it changed, OR if 0.25 seconds have passed (keep-alive heartbeat)
        if command != last_command or (current_time - last_send_time > 0.25):
            success = send_command(command)
            if command != last_command:
                if connected:
                    status = "✓ SENT" if success else "✗ FAILED"
                    print(f"{status}: Gesture {fingers} -> Command: {command}", flush=True)
                else:
                    print(f"OFFLINE: Gesture {fingers} -> Command: {command} (HC-05 not connected)", flush=True)
            last_command = command
            last_send_time = current_time

        # Draw landmarks (same as before)
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Display info on screen
        status_color = (0, 255, 0) if connected else (0, 0, 255)
        status_text = "HC-05: CONNECTED" if connected else "HC-05: OFFLINE"
        cv2.putText(img, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, status_color, 2)
        cv2.putText(img, f"Command: {command}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 255, 0), 2)
        cv2.putText(img, f"Fingers: {fingers}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 0), 2)
    else:
        # No hand detected - Stop the car!
        command = 'S'
        current_time = time.time()
        if command != last_command or (current_time - last_send_time > 0.25):
            success = send_command(command)
            if command != last_command:
                if connected:
                    status = "✓ SENT" if success else "✗ FAILED"
                    print(f"{status}: Hand lost -> Command: {command} (Stop)", flush=True)
            last_command = command
            last_send_time = current_time

        status_color = (0, 255, 0) if connected else (0, 0, 255)
        status_text = "HC-05: CONNECTED" if connected else "HC-05: OFFLINE"
        cv2.putText(img, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, status_color, 2)
        cv2.putText(img, "No hand detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 0, 255), 2)

    cv2.imshow("Hand Control Car", img)
    frame_count += 1
    
    # Show connection status every 30 frames
    if frame_count % 30 == 0:
        print(f"[Frame {frame_count}] HC-05 Status: {'Connected' if connected else 'Offline'}")
    
    if cv2.waitKey(1) == ord('q'):
        break

print("\n" + "="*50)
print("SHUTTING DOWN...")
cap.release()
cv2.destroyAllWindows()

# Close Bluetooth connection safely
if bluetooth:
    try:
        bluetooth.close()
        print("✓ Bluetooth connection closed")
    except:
        pass

print("✓ All systems shut down successfully")
print("="*50)
