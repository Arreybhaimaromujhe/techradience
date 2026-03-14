# Perfect Robot Car Wiring (Arduino + L298N + HC-05)

This guide shows a **stable wiring setup** for a Bluetooth controlled robot car using:

- Arduino Uno
- L298N Motor Driver
- HC-05 Bluetooth Module
- 2 DC Motors
- 2 × 18650 Batteries (7.4V pack)

---

# Power Wiring

## Battery → Motor Driver

18650 Battery Pack (7.4V)

Battery (+) → 12V / VCC on L298N  
Battery (-) → GND on L298N  

⚠️ All grounds must be connected together.

---

## Ground Connections

Battery (-) → L298N GND  
Arduino GND → L298N GND  

This **common ground** connection is critical.

---

# Motor Connections

Motor A (Left Wheel)

OUT1 → Motor wire  
OUT2 → Motor wire  

Motor B (Right Wheel)

OUT3 → Motor wire  
OUT4 → Motor wire  

---

# Arduino → Motor Driver Pins

Example control pins:

Arduino → L298N

D8  → IN1  
D9  → IN2  
D10 → IN3  
D11 → IN4  

ENA jumper → ON  
ENB jumper → ON  

(These jumpers enable the motors at full speed.)

---

# Bluetooth Module Wiring (HC-05)

HC-05 → Arduino

VCC → 5V  
GND → GND  
TXD → RX (Pin 0)  
RXD → TX (Pin 1)

⚠️ Important rule:

TX → RX  
RX → TX  

Never connect TX → TX.

---

# Optional Arduino Power Method

If the **5V_EN jumper** is present on the motor driver:

L298N 5V → Arduino 5V

This allows the battery pack to power the Arduino.

---

# Final Wiring Checklist

Before running the robot:

- Arduino GND connected to L298N GND
- Battery GND connected to L298N GND
- ENA jumper ON
- ENB jumper ON
- Motors connected to OUT1–OUT4
- HC-05 TX and RX crossed correctly

---

# Quick Test

1. Lift the robot so wheels are in the air.
2. Turn on battery power.
3. Connect Bluetooth from phone.
4. Send **forward command**.

Expected result:

Both wheels spin **same direction** and **same speed**.

---

# Components Used

- Arduino Uno
- L298N Motor Driver
- HC-05 Bluetooth Module
- DC Motors
- 18650 Lithium-ion Batteries

---

# Notes

This wiring is widely used in **robotics projects and competitions** because it is stable and simple to troubleshoot.
