# Foundations of IoT (25CS2741) – Laboratory Repository

## 1. Student & Course Information

- **Institution:** Shiv Nadar University Chennai
- **Course Code:** 25CS2741
- **Course Title:** Fundamentals of Internet of Things + Lab
- **Student Name:** P Deepak
- **Register Number:** 25011102072
- **Academic Term:** Semester 3

---

## 2. System Architecture & Platform Overview

This repository contains the complete, production-grade embedded C firmware, hardware schematics, register configurations, and technical documentation for all Continuous Assessment Test (CAT) modules across both foundational embedded hardware platforms:
1. **8051 Microcontroller Platform:** Bare-metal 8-bit CISC embedded programming, bitwise GPIO driver design, precise machine-cycle delay loops, Mode 1 hardware timers, asynchronous external hardware interrupts, multiplexed 7-segment displays, HD44780 LCD drivers, 4x4 keypad matrix decoders, and stepper/DC motor actuation drivers.
2. **STM32 ARM Cortex-M Platform:** High-performance 32-bit RISC microcontroller programming using STM32CubeMX HAL and ARM CMSIS drivers on STM32F103C8T6 (Blue Pill, 72 MHz) and STM32F401RET6 (Nucleo-64, 84 MHz). Demonstrates multi-channel hardware PWM, EXTI interrupt lines, USART asynchronous serial communication with ring buffers, bare-metal hardware I2C master protocols, Bosch Sensortec BME280 multi-variable compensation math, Wemos D1 Mini ESP8266 Wi-Fi AT modems, MQTT cloud streaming (broker.emqx.io), and Node-RED SCADA Dashboard 2.0 visualization.
3. **Capstone Mini-Project (CAT 15):** An automated civic decision-support system that processes ambient temperature, humidity, and barometric pressure data to forecast cyclonic front activity and autonomously trigger `CONDUCT SCHOOL` or `DECLARE HOLIDAY` advisories across a cloud web portal.

![Foundations of IoT System Architecture](circuit.png)

---

## 3. Comprehensive Master Index of Experiments

| Platform | Assessment | Task Identifier | Task Title & Objective | Target Hardware | Documentation Link |
|:---:|:---:|:---:|:---|:---:|:---:|
| **8051** | CAT 2 | `TASK2B` | Dual-Pattern LED Blinker with Re-entrant Delay | AT89C51 (11.0592 MHz) | [README.md](8051/CAT2/TASK2B/README.md) |
| **8051** | CAT 3 | `TASK3A` | Debounced Push-Button Counter with LED Status | AT89C51 (11.0592 MHz) | [README.md](8051/CAT3/TASK3A/README.md) |
| **8051** | CAT 4 | `TASK4A` | 1 kHz Square Wave via Timer 0 Mode 1 (16-bit) | AT89C51 (11.0592 MHz) | [README.md](8051/CAT4/TASK4A/README.md) |
| **8051** | CAT 5 | `TASK5A` | Hardware Interrupt-Driven E-Stop System via INT0 | AT89C51 (11.0592 MHz) | [README.md](8051/CAT5/TASK5A/README.md) |
| **8051** | CAT 5 | `TASK5B.1` | Static 0-9 Decimal Counter on Common Anode 7-Seg | AT89C51 (11.0592 MHz) | [README.md](8051/CAT5/TASK5B/TASK5B.1/README.md) |
| **8051** | CAT 5 | `TASK5B.2` | Dual-Digit Multiplexed 00-99 Display with POV | AT89C51 (11.0592 MHz) | [README.md](8051/CAT5/TASK5B/TASK5B.2/README.md) |
| **8051** | CAT 5 | `TASK5B.3` | 4-Digit Multiplexed Up/Down Counter with Switch | AT89C51 (11.0592 MHz) | [README.md](8051/CAT5/TASK5B/TASK5B.3/README.md) |
| **8051** | CAT 5 | `TASK5C` | 16x2 Character LCD Interfacing (HD44780) | AT89C51 (11.0592 MHz) | [README.md](8051/CAT5/TASK5C/README.md) |
| **8051** | CAT 6 | `TASK6A` | 4x4 Matrix Keypad Scanning with 7-Seg Display | AT89C51 (11.0592 MHz) | [README.md](8051/CAT6/TASK6A/README.md) |
| **8051** | CAT 6 | `TASK6B` | Keypad Door Lock Security with Passcode Check | AT89C51 (11.0592 MHz) | [README.md](8051/CAT6/TASK6B/README.md) |
| **8051** | CAT 7 | `TASK7A` | Stepper Motor Step Sequence via ULN2003 Driver | AT89C51 (11.0592 MHz) | [README.md](8051/CAT7/TASK7A/README.md) |
| **8051** | CAT 7 | `TASK7B` | Bidirectional Stepper Motor Speed Control | AT89C51 (11.0592 MHz) | [README.md](8051/CAT7/TASK7B/README.md) |
| **8051** | CAT 7 | `TASK7C` | Software PWM DC Motor Speed Controller (L293D) | AT89C51 (11.0592 MHz) | [README.md](8051/CAT7/TASK7C/README.md) |
| **STM32** | CAT 8 | `TASK8A` | Onboard LED Blinker with SysTick Timebase (PC13) | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT8/TASK8A/README.md) |
| **STM32** | CAT 8 | `TASK8B` | Push-Button Controlled LED Latch on PA0/PC13 | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT8/TASK8B/README.md) |
| **STM32** | CAT 8 | `TASK8C` | 4-Channel Ring Counter & Chaser on PA0-PA3 | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT8/TASK8C/README.md) |
| **STM32** | CAT 9 | `TASK9A` | STM32F401RE High-Performance 84 MHz Heartbeat | NUCLEO-F401RE (84 MHz) | [README.md](STM32/CAT9/TASK9A/README.md) |
| **STM32** | CAT 9 | `TASK9B` | EXTI13 Falling Edge Interrupt Controller (PC13) | NUCLEO-F401RE (84 MHz) | [README.md](STM32/CAT9/TASK9B/README.md) |
| **STM32** | CAT 10 | `TASK10A` | Hardware PWM Breathing LED on TIM2 Channel 1 | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT10/TASK10A/README.md) |
| **STM32** | CAT 10 | `TASK10B` | 50 Hz PWM RC Servo Motor Controller (0°-180°) | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT10/TASK10B/README.md) |
| **STM32** | CAT 10 | `TASK10C` | Dual-Channel Complementary PWM Motor Driver | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT10/TASK10C/README.md) |
| **STM32** | CAT 11 | `TASK11A` | USART2 Asynchronous Telemetry Link (115200 bps) | NUCLEO-F401RE (84 MHz) | [README.md](STM32/CAT11/TASK11A/README.md) |
| **STM32** | CAT 11 | `TASK11B` | Interrupt-Driven Interactive CLI Command Shell | NUCLEO-F401RE (84 MHz) | [README.md](STM32/CAT11/TASK11B/README.md) |
| **STM32** | CAT 12 | `TASK12A` | I2C1 Master Bus Initialization & Slave Scanner | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT12/TASK12A/README.md) |
| **STM32** | CAT 12 | `TASK12B` | Bosch BME280 Chip ID & Factory Trim Retrieval | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT12/TASK12B/README.md) |
| **STM32** | CAT 12 | `TASK12C` | Tri-Parameter Environmental Telemetry Math | STM32F103C8T6 (72 MHz) | [README.md](STM32/CAT12/TASK12C/README.md) |
| **STM32** | CAT 13 | `TASK13` | MQTT Telemetry Pipeline via ESP8266 Modem | STM32F103 + ESP8266 | [README.md](STM32/CAT13/TASK13/README.md) |
| **STM32** | CAT 14 | `TASK14` | Node-RED Real-Time Web Telemetry Visualization | STM32F103 + Node-RED | [README.md](STM32/CAT14/TASK14/README.md) |
| **STM32** | CAT 15 | `TASK15` | Automated School Monsoon Advisory System | NUCLEO-F401RE + Node-RED | [README.md](STM32/CAT15/TASK15/README.md) |

---

## 4. Repository Cleanliness & Verification Standards

- **Strict Directory Cleanliness:** All Continuous Assessment folders contain exclusively their designated task sub-directories with zero loose files.
- **Evaluator Script (`evaluate.py`):** An automated validation suite verifies the presence and integrity of all Keil project files (`.uvproj`, `.uvprojx`), C source files (`main.c`), startup code (`STARTUP.A51`, `startup_*.s`), CubeMX files (`.ioc`, `.mxproject`), compiled binaries (`.hex`), technical documentation (`README.md`), and high-resolution schematics (`circuit.png`).

To run the verification suite:
```bash
python evaluate.py
```
