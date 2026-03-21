# 🔌 Connections (ESP8266 NodeMCU)

## 🟢 MQ-3 Gas Sensor
- VCC → Vin (5V)
- GND → GND
- A0 → A0

---

## 🔵 Ultrasonic Sensor (HC-SR04)
- VCC → Vin (5V)
- GND → GND
- TRIG → D5 (GPIO14)
- ECHO → D6 (GPIO12) ⚠️ via voltage divider

### Voltage Divider (IMPORTANT)
- ECHO → 1kΩ resistor → D6
- D6 → 2kΩ resistor → GND

---

## 🟡 I2C LCD
- VCC → Vin (5V)
- GND → GND
- SDA → D2 (GPIO4)
- SCL → D1 (GPIO5)

---

## 🔴 Buzzer
- + → D7 (GPIO13)
- - → GND

---

## ⚡ Power
- Use USB / Power bank → NodeMCU
- OR Battery (+) → Switch → Vin
- Battery (-) → GND

---

## 🧠 Notes
- All GND must be common
- MQ3 needs 1–2 min warmup
- LCD address: 0x27 or 0x3F
- ESP8266 works on 3.3V logic (be careful with 5V signals)

---

## 🚀 Pin Summary
| Component | Pin |
|----------|-----|
| MQ3 | A0 |
| TRIG | D5 |
| ECHO | D6 |
| LCD SDA | D2 |
| LCD SCL | D1 |
| BUZZER | D7 |

