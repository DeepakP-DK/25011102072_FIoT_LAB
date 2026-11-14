# Foundations of IoT (25CS2741) – Laboratory Repository

## 1. Student & Course Information
- **Institution:** Shiv Nadar University Chennai
- **Department:** Computer Science & Engineering
- **Course:** Fundamentals of Internet of Things + Lab (25CS2741)
- **Student:** P Deepak
- **Register Number:** 25011102072
- **Semester:** 3

---

## 2. Laboratory Overview

This repository contains the 8051 and STM32 experiments completed for the Foundations of IoT laboratory, including embedded C programs, project files, circuit diagrams, and task-wise documentation.

The experiments cover GPIO, timers, interrupts, displays, keypads, motors, PWM, UART, I2C, sensors, Wi-Fi, MQTT, and Node-RED.

### Platforms
- **8051:** AT89C51 / AT89S52, 11.0592 MHz, Keil µVision C51.
- **STM32:** STM32F103C8T6 (72 MHz) and NUCLEO-F401RE (84 MHz), STM32CubeMX and Keil MDK-ARM.
- **IoT integration:** BME280, ESP8266, MQTT broker, and Node-RED dashboard.

### Capstone Project – CAT 15
**Automated Weather Monitoring and School Advisory System**

Uses the NUCLEO-F401RE, BME280, ESP8266, MQTT, and Node-RED to monitor environmental conditions and display school advisory alerts.

![Foundations of IoT System Architecture](circuit.png)

---

## 3. Master Index of Experiments

Each task folder contains its experiment documentation, source code, project files, and circuit diagram.

### 8051 Microcontroller Platform (CAT 2 to CAT 7)

| Assessment | Task ID | Experiment Title & Technical Objective | Target MCU / Clock | Documentation Link |
|:---:|:---:|:---|:---:|:---:|
| **CAT 2** | `TASK2A` | 8051 Minimum-System Bring-Up and Port-1 LED Proof Test | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT2/TASK2A/README.md) |
| **CAT 2** | `TASK2B` | Dual-Pattern LED Blinker with Re-entrant Delay Loops | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT2/TASK2B/README.md) |
| **CAT 2** | `TASK2C` | Calibrated Software Delay and GPIO Timing Test | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT2/TASK2C/README.md) |
| **CAT 3** | `TASK3A` | Debounced Push-Button Counter with LED Status Indication | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT3/TASK3A/README.md) |
| **CAT 3** | `TASK3B` | Four-Bit Binary LED Counter | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT3/TASK3B/README.md) |
| **CAT 3** | `TASK3C` | Alternating Four-LED Pattern Generator | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT3/TASK3C/README.md) |
| **CAT 3** | `TASK3D` | Synchronous Four-LED Flash Controller | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT3/TASK3D/README.md) |
| **CAT 4** | `TASK4A` | 1 kHz Symmetrical Square Wave via Timer 0 Mode 1 (16-bit) | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT4/TASK4A/README.md) |
| **CAT 4** | `TASK4B` | 4x4 Matrix Keypad Controlled LED Selector | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT4/TASK4B/README.md) |
| **CAT 5** | `TASK5A` | Hardware Interrupt-Driven Emergency Stop via INT0 Vector | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT5/TASK5A/README.md) |
| **CAT 5** | `TASK5B.1` | Static Single-Digit 0-9 Decimal Counter on Common Anode 7-Seg | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT5/TASK5B/TASK5B.1/README.md) |
| **CAT 5** | `TASK5B.2` | Dual-Digit Multiplexed 00-99 Display with Persistence of Vision | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT5/TASK5B/TASK5B.2/README.md) |
| **CAT 5** | `TASK5B.3` | 4-Digit Multiplexed Up/Down Counter with Direction Switch | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT5/TASK5B/TASK5B.3/README.md) |
| **CAT 5** | `TASK5C` | 16x2 Character Alphanumeric LCD Interfacing (HD44780 Driver) | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT5/TASK5C/README.md) |
| **CAT 6** | `TASK6A` | 4x4 Matrix Keypad Scanning with 7-Segment Hex Character Display | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT6/TASK6A/README.md) |
| **CAT 6** | `TASK6B` | Electronic Keypad Door Lock Security with Passcode Validation | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT6/TASK6B/README.md) |
| **CAT 7** | `TASK7A` | Unipolar Stepper Motor Step Sequence via ULN2003 Driver | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT7/TASK7A/README.md) |
| **CAT 7** | `TASK7B` | Bidirectional Stepper Motor Speed Control via Half-Stepping | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT7/TASK7B/README.md) |
| **CAT 7** | `TASK7C` | Software PWM DC Motor Speed Controller with L293D H-Bridge | AT89C51 @ 11.0592 MHz | [README.md](8051/CAT7/TASK7C/README.md) |

### STM32 ARM Cortex-M Platform (CAT 8 to CAT 15)

| Assessment | Task ID | Experiment Title & Technical Objective | Target MCU / Clock | Documentation Link |
|:---:|:---:|:---|:---:|:---:|
| **CAT 8** | `TASK8A` | STM32 Blue Pill GPIO Bring-Up & Onboard LED Blink on PC13 | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT8/TASK8A/README.md) |
| **CAT 8** | `TASK8B` | Push-Button Controlled LED Latch with Software Debouncing | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT8/TASK8B/README.md) |
| **CAT 8** | `TASK8C` | 4-Channel High-Speed Ring Counter & Chaser on PA0 - PA3 | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT8/TASK8C/README.md) |
| **CAT 9** | `TASK9A` | STM32F401RE High-Performance 84 MHz Heartbeat on LD2 (PA5) | NUCLEO-F401RE @ 84 MHz | [README.md](STM32/CAT9/TASK9A/README.md) |
| **CAT 9** | `TASK9B` | EXTI13 Falling Edge Interrupt Controller on PC13 with WFI | NUCLEO-F401RE @ 84 MHz | [README.md](STM32/CAT9/TASK9B/README.md) |
| **CAT 10** | `TASK10A` | Hardware PWM Breathing LED Controller Using TIM2 Channel 1 | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT10/TASK10A/README.md) |
| **CAT 10** | `TASK10B` | 50 Hz Precision PWM RC Servo Motor Angle Controller (0°-180°) | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT10/TASK10B/README.md) |
| **CAT 10** | `TASK10C` | Dual-Channel Complementary PWM Motor Driver on TIM2 CH3/CH4 | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT10/TASK10C/README.md) |
| **CAT 11** | `TASK11A` | USART2 Asynchronous Serial Telemetry Link (115200 bps) | NUCLEO-F401RE @ 84 MHz | [README.md](STM32/CAT11/TASK11A/README.md) |
| **CAT 11** | `TASK11B` | Interrupt-Driven Interactive CLI Command Shell via USART2 | NUCLEO-F401RE @ 84 MHz | [README.md](STM32/CAT11/TASK11B/README.md) |
| **CAT 12** | `TASK12A` | I2C1 Hardware Master Bus Initialization & Slave Address Scanner | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT12/TASK12A/README.md) |
| **CAT 12** | `TASK12B` | Bosch BME280 Silicon Chip ID & Factory Calibration Download | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT12/TASK12B/README.md) |
| **CAT 12** | `TASK12C` | Calibrated Tri-Parameter Environmental Telemetry Math (T, P, H) | STM32F103C8T6 @ 72 MHz | [README.md](STM32/CAT12/TASK12C/README.md) |
| **CAT 13** | `TASK13` | End-to-End MQTT Cloud Telemetry Pipeline via ESP8266 Modem | STM32F103 + ESP8266 | [README.md](STM32/CAT13/TASK13/README.md) |
| **CAT 14** | `TASK14` | Real-Time Node-RED Web UI Telemetry Visualization & Gauges | STM32F103 + Node-RED | [README.md](STM32/CAT14/TASK14/README.md) |
| **CAT 15** | `TASK15` | Capstone: Automated School Monsoon Advisory Decision System | NUCLEO-F401RE + Node-RED | [README.md](STM32/CAT15/TASK15/README.md) |

---

## 4. Hardware & Software

### Hardware
- AT89C51 / AT89S52 8051 development board.
- STM32F103C8T6 Blue Pill and NUCLEO-F401RE.
- ST-LINK programmer/debugger.
- BME280 sensor, ESP8266, servo, stepper motor, DC motors, LCD, 7-segment display, and keypad.

### Software
- Keil µVision C51 and Keil MDK-ARM.
- STM32CubeMX, HAL, and CMSIS.
- Node-RED Dashboard 2.0 and MQTT broker.
- PuTTY, TeraTerm, or RealTerm for serial debugging.

---

## 5. Submission Validation

Run the evaluator from the repository root:

```bash
python evaluate.py
```

It checks the required folders and files, including task documentation, source/project files, build outputs, and circuit diagrams.
