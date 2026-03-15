# Gesture Controlled Robot -- System Working Flow

This document explains the **complete working pipeline** of the
gesture-controlled robot system used in the project.

The robot uses **Computer Vision + AI + Bluetooth communication +
Arduino motor control** to convert hand gestures into robot movement.

------------------------------------------------------------------------

# System Architecture Overview

Camera → OpenCV → MediaPipe → Finger Detection → Gesture Mapping →
Bluetooth → Arduino → Motor Driver → Motors

------------------------------------------------------------------------

# 1. Camera Captures Hand Image

The laptop camera continuously captures live frames.

Example code:

``` python
cap = cv2.VideoCapture(0)
success, img = cap.read()
```

This frame is used as the input for gesture recognition.

------------------------------------------------------------------------

# 2. Image Processing using OpenCV

OpenCV processes the frame and converts it into RGB format for AI
processing.

``` python
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

OpenCV is responsible for:

-   Capturing frames
-   Frame flipping
-   Image color conversion
-   Displaying results

------------------------------------------------------------------------

# 3. Hand Detection using MediaPipe

MediaPipe detects the hand and extracts **21 landmark points**.

``` python
results = hands.process(img_rgb)
```

These landmarks represent key points such as:

-   Finger tips
-   Finger joints
-   Palm base

This makes gesture detection highly accurate.

------------------------------------------------------------------------

# 4. Finger State Detection

The program determines whether each finger is **up (1)** or **down
(0)**.

Example:

Index finger up\
Middle finger down\
Ring finger down\
Pinky down\
Thumb down

Converted into:

    [0,1,0,0,0]

This is called a **binary finger array**.

------------------------------------------------------------------------

# 5. Gesture to Command Conversion

The binary finger array is mapped to robot commands.

Example mapping:

  Gesture         Command   Action
  --------------- --------- ----------
  \[0,1,0,0,0\]   F         Forward
  \[0,1,1,0,0\]   B         Backward
  \[0,1,0,0,1\]   L         Left
  \[0,1,1,1,1\]   R         Right
  Other           S         Stop

Example function:

``` python
def get_command(fingers):
    if fingers == [0,1,0,0,0]:
        return 'F'
    elif fingers == [0,1,1,0,0]:
        return 'B'
    elif fingers == [0,1,0,0,1]:
        return 'L'
    elif fingers == [0,1,1,1,1]:
        return 'R'
    else:
        return 'S'
```

------------------------------------------------------------------------

# 6. Command Sent via Bluetooth

The command is transmitted using the **HC-05 Bluetooth module**.

``` python
bluetooth.write(command.encode())
```

Example data sent:

    F
    B
    L
    R
    S

------------------------------------------------------------------------

# 7. Arduino Receives the Command

The Arduino UNO reads the incoming serial command.

Example:

``` cpp
char cmd = Serial.read();
```

The Arduino interprets this command to control the motors.

------------------------------------------------------------------------

# 8. Motor Driver Control

The Arduino sends signals to the **L298N Motor Driver**.

Example:

-   F → Both motors forward
-   B → Both motors backward
-   L → Right motor forward
-   R → Left motor forward
-   S → Stop

------------------------------------------------------------------------

# 9. Robot Movement

The motor driver powers the **two DC motors of the 2WD chassis**,
causing the robot to move according to the gesture.

Movement types:

-   Forward
-   Backward
-   Left turn
-   Right turn
-   Stop

------------------------------------------------------------------------

# Complete Data Flow

    Camera
    ↓
    OpenCV Processing
    ↓
    MediaPipe Hand Detection
    ↓
    Finger Binary Array
    ↓
    Gesture Command Mapping
    ↓
    Bluetooth Transmission (HC‑05)
    ↓
    Arduino UNO
    ↓
    Motor Driver (L298N)
    ↓
    DC Motors
    ↓
    Robot Movement

------------------------------------------------------------------------

# Why MediaPipe Was Used

MediaPipe was chosen because:

-   Provides **21 hand landmark points**
-   Works **in real time**
-   High accuracy gesture detection
-   Faster than traditional contour-based hand detection

This makes the system reliable for **human-robot interaction**.

------------------------------------------------------------------------

# Summary

The system converts **human gestures into robot movement** using
computer vision and embedded control.

Technologies used:

-   OpenCV
-   MediaPipe
-   Python
-   Bluetooth HC‑05
-   Arduino UNO
-   L298N Motor Driver
-   2WD Robot Chassis

This architecture enables **touchless robot control**, useful for
applications in healthcare, industry, and hazardous environments.
