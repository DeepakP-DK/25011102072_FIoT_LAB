# Foundations of IoT (25CS2741) – Lab Portfolio

## Student Details
- **Name:** P Deepak
- **Register No.:** 25011102072
- **Programme:** B.Tech – Computer Science and Engineering (IoT)
- **Institution:** Shiv Nadar University Chennai
- **Semester:** 3

## About
This repository contains the 8051 and STM32 experiments completed for the Foundations of IoT laboratory. Each task folder includes its available source code, project/configuration files, circuit diagram, and experiment documentation.

## Repository Structure
- `8051/` – 8051 microcontroller experiments (CAT 2–7)
- `STM32/` – STM32 microcontroller experiments (CAT 8–15)
- `README.md` – Repository overview and task index
- `circuit.png` – Overall system architecture
- `evaluate.py` – Submission validation script

![IoT Lab System Architecture](circuit.png)

## Task Index

### 8051
| CAT | Task |
|---|---|
| CAT 2 | TASK2B |
| CAT 3 | TASK3A |
| CAT 4 | TASK4A |
| CAT 5 | TASK5A, TASK5B.1, TASK5B.2, TASK5B.3, TASK5C |
| CAT 6 | TASK6A, TASK6B |
| CAT 7 | TASK7A, TASK7B, TASK7C |

### STM32
| CAT | Task |
|---|---|
| CAT 8 | TASK8A, TASK8B, TASK8C |
| CAT 9 | TASK9A, TASK9B |
| CAT 10 | TASK10A, TASK10B, TASK10C |
| CAT 11 | TASK11A, TASK11B |
| CAT 12 | TASK12A, TASK12B, TASK12C |
| CAT 13 | TASK13 |
| CAT 14 | TASK14 |
| CAT 15 | TASK15 |

## Tools & Platforms
- **8051:** AT89C51, Keil µVision
- **STM32:** STM32F103C8T6 / NUCLEO-F401RE, STM32CubeMX, Keil MDK-ARM
- **IoT:** BME280, ESP8266, MQTT, Node-RED

## Run the Evaluator
From the repository root, run:

```bash
python evaluate.py
```

The script checks the required task folders and submission files.
