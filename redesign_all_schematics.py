import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

SCHEMATIC_SPECS = [
    # 8051 TASKS
    {
        "task_id": "TASK2B",
        "path": "8051/CAT2/TASK2B/circuit.png",
        "title": "Dual-Pattern LED Blinker with Re-entrant Delay",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Architecture (12 Clocks/Machine Cycle)",
        "pwr_vcc": "+5.0V DC Regulated (Pin 40 VCC)",
        "pwr_reset": "Power-On Reset (10uF Cap + 10k Resistor to RST Pin 9)",
        "clock_source": "11.0592 MHz Quartz Crystal (XTAL1 Pin 19, XTAL2 Pin 18)",
        "clock_timing": "1.085 us Machine Cycle Timebase",
        "pin_details": [
            "P1.0 - P1.7: Configured as Active-LOW Output Bus",
            "EA/VPP (Pin 31): Tied to +5V (Internal ROM Execution)",
            "ALE/PROG (Pin 30) & PSEN (Pin 29): Left Unconnected"
        ],
        "internal_modules": [
            "Port 1 Output Latch Register (SFR 0x90)",
            "Software Re-entrant Delay Subroutine (DJNZ execution)"
        ],
        "periph_list": [
            "8-Segment LED Bar Array (Active-LOW Common Anode)",
            "8x 330 Ohm Current-Limiting Resistors",
            "11.0592 MHz Crystal Oscillator + 2x 22pF Capacitors"
        ],
        "conn_specs": [
            "P1.0..P1.7 -> 330 Ohm Resistors -> LED Cathodes",
            "LED Anodes -> Common +5V Power Rail",
            "RST Pin 9 -> Push-Button to VCC & 10k to GND"
        ]
    },
    {
        "task_id": "TASK3A",
        "path": "8051/CAT3/TASK3A/circuit.png",
        "title": "Debounced Push-Button Counter with LED Status Indication",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Architecture (Standard 8051 Core)",
        "pwr_vcc": "+5.0V DC Stable Rail (Pin 40)",
        "pwr_reset": "RC Power-On Reset Circuit (Pin 9)",
        "clock_source": "11.0592 MHz Quartz Crystal Oscillator",
        "clock_timing": "12 Clocks/Cycle (1.085 us per cycle)",
        "pin_details": [
            "P3.2 (INT0 / GPIO): Tactile Switch Input (Active-LOW)",
            "P1.0 - P1.3: 4-Bit Binary Counter Output Nibble",
            "EA/VPP (Pin 31): Pulled HIGH to +5V Rail"
        ],
        "internal_modules": [
            "Port 3 Input Buffer with 10k External Pull-Up",
            "Software Contact Bounce Filter (20ms Re-sampling window)"
        ],
        "periph_list": [
            "Momentary Tactile Push-Button Switch",
            "10k Ohm External Pull-Up Resistor",
            "4x Green User LEDs with 330 Ohm Resistors"
        ],
        "conn_specs": [
            "Tactile Switch -> P3.2 and Ground (GND)",
            "10k Resistor -> Between P3.2 and +5V",
            "P1.0..P1.3 -> 330 Ohm Resistors -> LED Cathodes"
        ]
    },
    {
        "task_id": "TASK4A",
        "path": "8051/CAT4/TASK4A/circuit.png",
        "title": "1 kHz Square Wave Generation via Timer 0 Mode 1 (16-bit)",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Architecture",
        "pwr_vcc": "+5.0V DC Power Supply Rail",
        "pwr_reset": "Hardware Reset Circuit (RST Pin 9)",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "500 us Half-Period (Reload: 0xFE33)",
        "pin_details": [
            "P1.5: Symmetrical Square Wave Frequency Output Pin",
            "EA Pin 31: Tied to +5V (Internal Flash Mode)",
            "XTAL1 & XTAL2: Pins 19 & 18 with 22pF Loading Caps"
        ],
        "internal_modules": [
            "Hardware Timer 0 configured in Mode 1 (16-bit Timer)",
            "TMOD Register (0x01) & TF0 Overflow Flag Polling"
        ],
        "periph_list": [
            "Digital Storage Oscilloscope (DSO) Test Point",
            "11.0592 MHz Crystal + 2x 22pF Ceramic Capacitors",
            "Status Indicator LED on Output Pin P1.5"
        ],
        "conn_specs": [
            "P1.5 -> DSO Probe Channel 1 (BNC Coaxial)",
            "DSO Ground Clip -> Common Circuit Ground (GND)",
            "P1.5 -> 1k Ohm Resistor -> LED Indicator"
        ]
    },
    {
        "task_id": "TASK5A",
        "path": "8051/CAT5/TASK5A/circuit.png",
        "title": "Hardware Interrupt-Driven Emergency Stop System via INT0",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC with 2-Level Interrupt Controller",
        "pwr_vcc": "+5.0V DC Main Supply Rail",
        "pwr_reset": "RC Reset Network on Pin 9",
        "clock_source": "11.0592 MHz Quartz Crystal",
        "clock_timing": "Sub-microsecond Interrupt Vector Latency",
        "pin_details": [
            "P3.2 (/INT0 Pin 12): External Interrupt 0 (Falling-Edge)",
            "P1.0: Normal Background Heartbeat Running LED",
            "P1.7: Latched Emergency Alarm Indicator / Buzzer"
        ],
        "internal_modules": [
            "Interrupt Vector 0x0003 (External Interrupt 0 ISR)",
            "TCON Register (IT0 = 1) & IE Register (EX0 = 1, EA = 1)"
        ],
        "periph_list": [
            "Emergency Stop Push-Button Switch (Normally Open)",
            "10k Pull-up Resistor to +5V",
            "Red Alarm LED + Active 5V Piezo Buzzer"
        ],
        "conn_specs": [
            "E-Stop Button -> P3.2 and GND",
            "P1.0 -> 330 Ohm -> Normal Running Green LED",
            "P1.7 -> 330 Ohm -> Red Alarm LED & Piezo Driver"
        ]
    },
    {
        "task_id": "TASK5B.1",
        "path": "8051/CAT5/TASK5B/TASK5B.1/circuit.png",
        "title": "Static Single-Digit 0-9 Decimal Counter on Common Anode 7-Segment",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Core",
        "pwr_vcc": "+5.0V DC Regulated Bus",
        "pwr_reset": "RC Power-On Reset on Pin 9",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "1-Second Incremental Decimal Timebase",
        "pin_details": [
            "P2.0 - P2.6: 7-Segment Data Lines (a, b, c, d, e, f, g)",
            "P2.7: Decimal Point (DP) Segment Line",
            "EA Pin 31: Tied to +5V"
        ],
        "internal_modules": [
            "Port 2 Output Driver (Active-LOW Segment Encoding)",
            "Code Memory Lookup Table for Numerals 0 to 9"
        ],
        "periph_list": [
            "Common Anode 0.56-inch 7-Segment LED Display",
            "7x 220 Ohm Current-Limiting Resistors",
            "Filtered +5V DC Anode Power Rail"
        ],
        "conn_specs": [
            "P2.0..P2.6 -> 220 Ohm Resistors -> Display Segments a..g",
            "Display Common Anode Terminal -> +5V Supply Rail",
            "RST -> 10k to GND & 10uF to +5V"
        ]
    },
    {
        "task_id": "TASK5B.2",
        "path": "8051/CAT5/TASK5B/TASK5B.2/circuit.png",
        "title": "Dual-Digit Multiplexed 00-99 Display with Persistence of Vision (POV)",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Core",
        "pwr_vcc": "+5.0V DC Main Rail",
        "pwr_reset": "Hardware Reset Circuit on Pin 9",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "100 Hz Flicker-Free Multiplexing Frame Rate",
        "pin_details": [
            "P2.0 - P2.6: Shared Segment Data Bus (a - g)",
            "P1.0: Digit 1 Enable Driver (Tens Digit)",
            "P1.1: Digit 2 Enable Driver (Units Digit)"
        ],
        "internal_modules": [
            "Time-Division Multiplex Scanning Routine",
            "Anti-Ghosting Display Blanking State Engine"
        ],
        "periph_list": [
            "Dual-Digit Common Cathode 7-Segment Display Module",
            "2x BC547 NPN Digit Switching Transistors",
            "7x 220 Ohm Segment Resistors + 2x 1k Base Resistors"
        ],
        "conn_specs": [
            "P2.0..P2.6 -> 220 Ohm -> Shared Segments a..g",
            "P1.0 -> 1k Ohm -> Base Q1 (Digit 1 Cathode to GND)",
            "P1.1 -> 1k Ohm -> Base Q2 (Digit 2 Cathode to GND)"
        ]
    },
    {
        "task_id": "TASK5B.3",
        "path": "8051/CAT5/TASK5B/TASK5B.3/circuit.png",
        "title": "4-Digit Multiplexed Up/Down Counter with Direction Control Switch",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Architecture",
        "pwr_vcc": "+5.0V DC Power Supply Rail",
        "pwr_reset": "Standard RC Reset Network",
        "clock_source": "11.0592 MHz Crystal",
        "clock_timing": "250 Hz Continuous Refresh Cycle",
        "pin_details": [
            "P0.0 - P0.6: 7-Segment Segment Bus (External Pull-Ups)",
            "P2.0 - P2.3: 4-Digit Active-LOW Transistor Selectors",
            "P3.3: Direction Control Toggle Switch (1=UP, 0=DOWN)"
        ],
        "internal_modules": [
            "Port 0 Open-Drain Bus Driver with 10k Resistor Pack",
            "Modular Arithmetic Digit Decomposer (Thousands/Hundreds/Tens/Units)"
        ],
        "periph_list": [
            "4-Digit Common Cathode 7-Segment Display Module",
            "4x S8050 NPN Driver Transistors",
            "8-Pin 10k Resistor Network (RP1 Pull-up for Port 0)"
        ],
        "conn_specs": [
            "Port 0 -> RP1 Pull-Up Array -> Display Segments a..g",
            "P2.0..P2.3 -> 1k Base Resistors -> Q1..Q4 Common Cathodes",
            "P3.3 -> SPST Direction Switch to Ground"
        ]
    },
    {
        "task_id": "TASK5C",
        "path": "8051/CAT5/TASK5C/circuit.png",
        "title": "16x2 Character LCD Interfacing (HD44780 Controller)",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Architecture",
        "pwr_vcc": "+5.0V DC Logic & Backlight Rail",
        "pwr_reset": "Hardware Power-On Reset Circuit",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "Calibrated Enable Pulse Timebase (>450ns)",
        "pin_details": [
            "P2.0 - P2.7: 8-Bit Bidirectional LCD Data Bus (D0 - D7)",
            "P3.5: Register Select (RS: 0=Command, 1=Data)",
            "P3.6: Read/Write (RW: 0=Write, 1=Read)",
            "P3.7: Enable Strobe (EN: Falling-Edge Triggered)"
        ],
        "internal_modules": [
            "HD44780 Protocol Command Engine (0x38, 0x0C, 0x06, 0x01)",
            "String Serialization & DDRAM Line Addressing Driver"
        ],
        "periph_list": [
            "16x2 Alphanumeric LCD Module (Hitachi HD44780)",
            "10k Single-Turn Trimpot for Contrast (V0 Pin 3)",
            "LED Backlight Power Rails (Pin 15 Anode, Pin 16 Cathode)"
        ],
        "conn_specs": [
            "P2.0..P2.7 -> LCD Data Pins D0..D7 (Pins 7..14)",
            "P3.5 -> LCD RS (Pin 4), P3.6 -> LCD RW (Pin 5), P3.7 -> LCD EN (Pin 6)",
            "Trimpot Center Wiper -> LCD V0 (Pin 3 Contrast)"
        ]
    },
    {
        "task_id": "TASK6A",
        "path": "8051/CAT6/TASK6A/circuit.png",
        "title": "4x4 Matrix Keypad Scanning with 7-Segment Hexadecimal Display",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Architecture",
        "pwr_vcc": "+5.0V DC Main Rail",
        "pwr_reset": "RC Power-On Reset on Pin 9",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "Sequential Row Strobe & Debounce Scanning",
        "pin_details": [
            "P1.0 - P1.3: Keypad Row Outputs (R1 - R4 Active-LOW)",
            "P1.4 - P1.7: Keypad Column Inputs (C1 - C4 with Pull-Ups)",
            "P2.0 - P2.6: Decoded Hex Character Output to 7-Segment Display"
        ],
        "internal_modules": [
            "2D Matrix Row Strobe & Column Sense Scanning Logic",
            "Hardware Debouncing & 16-Character Hex Look-up Table"
        ],
        "periph_list": [
            "4x4 Matrix Membrane / Tactile Keypad Module",
            "10k Pull-up Resistor Network on Column Pins",
            "Common Anode 7-Segment Display + 7x 220 Ohm Resistors"
        ],
        "conn_specs": [
            "P1.0..P1.3 -> Keypad Row Terminals 1..4",
            "P1.4..P1.7 -> Keypad Column Terminals 5..8",
            "P2.0..P2.6 -> 220 Ohm Resistors -> 7-Segment Display Segments a..g"
        ]
    },
    {
        "task_id": "TASK6B",
        "path": "8051/CAT6/TASK6B/circuit.png",
        "title": "Electronic Keypad Door Lock Security System with Passcode Validation",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Architecture",
        "pwr_vcc": "+5.0V DC Power Supply Rail",
        "pwr_reset": "Hardware Power-On Reset Circuit",
        "clock_source": "11.0592 MHz Quartz Crystal",
        "clock_timing": "Real-Time Sequential Security State Engine",
        "pin_details": [
            "P1.0 - P1.7: 4x4 Keypad Row and Column Matrix Interface",
            "P3.3: Solenoid Door Latch Relay Output (Active-LOW)",
            "P3.4: Access Denied Audio Alert Buzzer Output"
        ],
        "internal_modules": [
            "Security Passcode Verification State Machine",
            "Timed Relay Energization Pulse Generator (3.0 seconds)"
        ],
        "periph_list": [
            "4x4 Matrix Keypad Assembly",
            "5V SPDT Relay Module with Flyback Diode & NPN Driver",
            "5V Active Piezo Buzzer & Bicolor Status LEDs"
        ],
        "conn_specs": [
            "P1.0..P1.7 -> 4x4 Matrix Keypad",
            "P3.3 -> Relay Module Signal Input (Controls 12V Solenoid)",
            "P3.4 -> Piezo Buzzer Driver Circuit"
        ]
    },
    {
        "task_id": "TASK7A",
        "path": "8051/CAT7/TASK7A/circuit.png",
        "title": "Unipolar Stepper Motor Step Sequence Control via ULN2003 Driver",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Architecture",
        "pwr_vcc": "+5.0V Logic & Dedicated +5V 1A Motor Rail",
        "pwr_reset": "RC Power-On Reset on Pin 9",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "Calibrated 15ms Inter-Step Torque Delay",
        "pin_details": [
            "P2.0 - P2.3: Stator Coil Drive Signals (Phase A, B, C, D)",
            "EA/VPP (Pin 31): Tied to +5V VCC",
            "Common GND: MCU GND tied to Motor Power Supply GND"
        ],
        "internal_modules": [
            "4-Step Full-Step Phase Commutation Table (0x09, 0x0C, 0x06, 0x03)",
            "Sequential Output Commutator Engine"
        ],
        "periph_list": [
            "28BYJ-48 5V 4-Phase Unipolar Stepper Motor",
            "ULN2003A 7-Channel Darlington Driver IC Module",
            "External 5V 1.0A DC Power Adapter"
        ],
        "conn_specs": [
            "P2.0..P2.3 -> ULN2003 Inputs IN1..IN4",
            "ULN2003 Outputs OUT1..OUT4 -> Stepper Connector (Blue, Pink, Yellow, Orange)",
            "Motor Red Lead -> +5V External Motor Power Rail"
        ]
    },
    {
        "task_id": "TASK7B",
        "path": "8051/CAT7/TASK7B/circuit.png",
        "title": "Bidirectional Stepper Motor Speed Control with Half-Stepping",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Architecture",
        "pwr_vcc": "+5.0V Logic & +5V Motor Rails",
        "pwr_reset": "Standard RC Reset Network",
        "clock_source": "11.0592 MHz Crystal",
        "clock_timing": "Dynamic Inter-Step Speed Timebase (5ms to 15ms)",
        "pin_details": [
            "P2.0 - P2.3: 4-Phase Stepper Commutation Lines (IN1 - IN4)",
            "P3.2: Direction Control Switch (CW / CCW)",
            "P3.3: Speed Selection Switch (High Speed / Low Speed)"
        ],
        "internal_modules": [
            "8-Step Half-Stepping Commutation Ring Buffer",
            "Reversible Table Pointer with Boundary Clamping"
        ],
        "periph_list": [
            "28BYJ-48 Stepper Motor + ULN2003 Driver Board",
            "2x SPST Toggle Switches with 10k Pull-Ups",
            "Phase Indicator LEDs on ULN2003 Board"
        ],
        "conn_specs": [
            "P2.0..P2.3 -> ULN2003 Inputs IN1..IN4",
            "P3.2 -> Direction Switch to GND (10k Pull-up to +5V)",
            "P3.3 -> Speed Switch to GND (10k Pull-up to +5V)"
        ]
    },
    {
        "task_id": "TASK7C",
        "path": "8051/CAT7/TASK7C/circuit.png",
        "title": "Software PWM DC Motor Speed Controller with L293D H-Bridge",
        "mcu_name": "AT89C51 / AT89S52",
        "mcu_arch": "8-bit CISC Microcontroller Architecture",
        "pwr_vcc": "+5.0V Logic (VCC1) & +9V/12V Motor Rail (VCC2)",
        "pwr_reset": "Hardware RC Reset on Pin 9",
        "clock_source": "11.0592 MHz Crystal Oscillator",
        "clock_timing": "100 Hz Software PWM Modulation Timebase",
        "pin_details": [
            "P2.0: H-Bridge Direction Input 1 (IN1 = HIGH)",
            "P2.1: H-Bridge Direction Input 2 (IN2 = LOW)",
            "P2.2: H-Bridge Enable 1 / PWM Duty Control Pin (EN1)"
        ],
        "internal_modules": [
            "Software PWM Duty Cycle Generator (25%, 50%, 75%, 100%)",
            "Bidirectional H-Bridge Direction Logic Controller"
        ],
        "periph_list": [
            "Small 5V-12V Brushed DC Electric Motor",
            "L293D Quadruple Half-H Motor Driver IC",
            "0.1uF Motor Noise Suppression Ceramic Capacitor"
        ],
        "conn_specs": [
            "P2.0 -> L293D Pin 2 (IN1), P2.1 -> L293D Pin 7 (IN2)",
            "P2.2 -> L293D Pin 1 (EN1 PWM Strobe)",
            "L293D Pins 3 & 6 (OUT1 & OUT2) -> DC Motor Terminals"
        ]
    },

    # STM32 TASKS
    {
        "task_id": "TASK8A",
        "path": "STM32/CAT8/TASK8A/circuit.png",
        "title": "Onboard LED Blinker with SysTick Timebase on PC13",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit RISC Core (72 MHz Maximum)",
        "pwr_vcc": "+3.3V DC Regulated from Onboard RT9193 LDO",
        "pwr_reset": "Internal Power-On Reset & NRST Button",
        "clock_source": "8.0 MHz External Crystal (HSE) -> 72 MHz via PLL",
        "clock_timing": "SysTick 1ms Hardware Tick Timebase",
        "pin_details": [
            "PC13: Configured as GPIO Output (Push-Pull, Low-Speed)",
            "PA13 / PA14: Serial Wire Debug (SWDIO / SWCLK to ST-Link)",
            "BOOT0 / BOOT1: Tied to GND for Normal Flash Execution"
        ],
        "internal_modules": [
            "GPIOC Peripheral Clock Gate (__HAL_RCC_GPIOC_CLK_ENABLE)",
            "Cortex-M3 SysTick Core Timer for HAL_Delay()"
        ],
        "periph_list": [
            "Onboard SMD User LED (Connected to PC13 through 510 Ohm to 3.3V)",
            "ST-LINK V2 Programmer / Debugger Dongle",
            "8.0 MHz Main Crystal & 32.768 kHz RTC Crystal"
        ],
        "conn_specs": [
            "PC13 -> Onboard LED Anode via 510 Ohm Resistor (Active-LOW)",
            "SWDIO / SWCLK -> ST-LINK V2 SWD Pins",
            "+3.3V / GND -> ST-LINK Power Terminals"
        ]
    },
    {
        "task_id": "TASK8B",
        "path": "STM32/CAT8/TASK8B/circuit.png",
        "title": "Push-Button Controlled LED Latch with Software Debouncing",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit RISC Processor",
        "pwr_vcc": "+3.3V DC Operating Rail",
        "pwr_reset": "Hardware NRST Network",
        "clock_source": "8.0 MHz HSE with PLL to 72 MHz",
        "clock_timing": "20ms Non-Blocking Software Debounce Window",
        "pin_details": [
            "PA0: GPIO Digital Input with Internal Pull-Up Resistor",
            "PC13: GPIO Output Push-Pull (Onboard Status LED)",
            "PA13/PA14: SWD Debug Interface"
        ],
        "internal_modules": [
            "GPIOA & GPIOC Peripheral Clock Controllers",
            "HAL_GPIO_ReadPin() & HAL_GPIO_TogglePin() Drivers"
        ],
        "periph_list": [
            "Momentary Tactile Push-Button Switch",
            "Internal 40k Pull-Up Resistor on PA0",
            "Onboard User Indicator LED on PC13"
        ],
        "conn_specs": [
            "Tactile Button Terminal 1 -> PA0",
            "Tactile Button Terminal 2 -> System Ground (GND)",
            "PC13 -> Onboard LED (Toggles on Valid Falling Edge)"
        ]
    },
    {
        "task_id": "TASK8C",
        "path": "STM32/CAT8/TASK8C/circuit.png",
        "title": "4-Channel Ring Counter & Chaser Display on PA0-PA3",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Architecture",
        "pwr_vcc": "+3.3V DC Power Bus",
        "pwr_reset": "Internal Power-On Reset & External Filter",
        "clock_source": "8.0 MHz HSE -> 72 MHz System Clock",
        "clock_timing": "150ms Synchronous Sequence Delay Interval",
        "pin_details": [
            "PA0, PA1, PA2, PA3: GPIO Outputs Push-Pull (High Speed)",
            "PC13: Heartbeat Indicator LED",
            "SWDIO / SWCLK: ST-LINK Programming Interface"
        ],
        "internal_modules": [
            "GPIOA Multi-Pin Parallel Bit-Set / Reset Register (BSRR)",
            "Array-Driven Sequential State Commutator"
        ],
        "periph_list": [
            "4x Color User LEDs (Red, Yellow, Green, Blue)",
            "4x 330 Ohm Current-Limiting Resistors",
            "Solderless Breadboard & Premium M-F Jumpers"
        ],
        "conn_specs": [
            "PA0..PA3 -> 330 Ohm Resistors -> LED Anodes",
            "LED Cathodes -> Common System Ground (GND)",
            "3.3V & GND -> Breadboard Power Rails"
        ]
    },
    {
        "task_id": "TASK9A",
        "path": "STM32/CAT9/TASK9A/circuit.png",
        "title": "STM32F401RE High-Performance 84 MHz Heartbeat on LD2 (PA5)",
        "mcu_name": "STM32F401RET6 (Nucleo-64)",
        "mcu_arch": "ARM Cortex-M4F with Hardware FPU (84 MHz Maximum)",
        "pwr_vcc": "+3.3V / +5V USB VBUS from ST-LINK/V2-1",
        "pwr_reset": "Hardware Black Push-Button (B2) on NRST",
        "clock_source": "16.0 MHz Internal HSI -> 84 MHz PLL Core Clock",
        "clock_timing": "SysTick 1ms Calibrated Real-Time Timebase",
        "pin_details": [
            "PA5: User LED LD2 Output (Push-Pull, High-Speed)",
            "PC13: User Push-Button B1 Input (Active-LOW)",
            "PA2 / PA3: ST-LINK Virtual COM Port (USART2 TX/RX)"
        ],
        "internal_modules": [
            "High-Speed Internal (HSI) RC Oscillator & PLL Multiplexer",
            "GPIOA Peripheral Clock & Flash Prefetch/Instruction Cache"
        ],
        "periph_list": [
            "Onboard High-Efficiency Green User LED LD2",
            "Onboard ST-LINK/V2-1 Integrated Debug Probe",
            "Morpho & Arduino Uno V3 Expansion Headers"
        ],
        "conn_specs": [
            "PA5 -> Internal PCB Trace -> Green User LED LD2",
            "PC13 -> Blue User Tactile Button B1 -> GND",
            "Mini-USB Port -> PC Host for Power and In-Circuit Debug"
        ]
    },
    {
        "task_id": "TASK9B",
        "path": "STM32/CAT9/TASK9B/circuit.png",
        "title": "EXTI13 Falling Edge Interrupt Controller on PC13",
        "mcu_name": "STM32F401RET6 (Nucleo-64)",
        "mcu_arch": "ARM Cortex-M4F with Nested Vectored Interrupt Controller (NVIC)",
        "pwr_vcc": "+3.3V DC System Operating Rail",
        "pwr_reset": "Hardware NRST Reset Button",
        "clock_source": "84 MHz PLL System Clock",
        "clock_timing": "Zero-Polling Asynchronous Interrupt Service Routine",
        "pin_details": [
            "PC13: Configured as EXTI Line 13 (Falling-Edge Triggered)",
            "PA5: Output to LD2 LED Indicator",
            "PA2/PA3: Telemetry Serial Console Link"
        ],
        "internal_modules": [
            "SYSCFG External Interrupt Line Router (EXTI15_10_IRQn)",
            "NVIC Priority Grouping & HAL_GPIO_EXTI_Callback Handler"
        ],
        "periph_list": [
            "Onboard Blue User Push-Button B1 (PC13)",
            "Onboard Green LED LD2 (PA5)",
            "ST-LINK VCP Serial Monitor Interface"
        ],
        "conn_specs": [
            "PC13 -> Blue Push-Button B1 -> GND",
            "Falling Edge on PC13 -> Hardware EXTI13 Trigger",
            "ISR Callback -> HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5)"
        ]
    },
    {
        "task_id": "TASK10A",
        "path": "STM32/CAT10/TASK10A/circuit.png",
        "title": "Hardware PWM Breathing LED Controller Using TIM2 Channel 1",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Architecture",
        "pwr_vcc": "+3.3V DC Main Rail",
        "pwr_reset": "Internal Power-On Reset & Filter",
        "clock_source": "72 MHz PLL Core Clock",
        "clock_timing": "1 kHz PWM Carrier Frequency (ARR=999, PSC=71)",
        "pin_details": [
            "PA0: TIM2_CH1 Alternate Function Push-Pull PWM Output",
            "PA13 / PA14: Serial Wire Debug Interface",
            "PC13: Status Heartbeat LED"
        ],
        "internal_modules": [
            "General Purpose Timer TIM2 in PWM Mode 1",
            "Capture/Compare Register 1 (CCR1) Dynamic Duty Modulation"
        ],
        "periph_list": [
            "High-Brightness 5mm Blue LED",
            "220 Ohm Current-Limiting Resistor",
            "Rigol / DSO Oscilloscope Test Probe"
        ],
        "conn_specs": [
            "PA0 (TIM2_CH1) -> 220 Ohm Resistor -> LED Anode",
            "LED Cathode -> Common Ground (GND)",
            "DSO Channel 1 -> PA0 (Monitors 1 kHz PWM waveform)"
        ]
    },
    {
        "task_id": "TASK10B",
        "path": "STM32/CAT10/TASK10B/circuit.png",
        "title": "50 Hz Precision PWM RC Servo Motor Controller (0° to 180°)",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Core",
        "pwr_vcc": "+3.3V MCU Logic & +5.0V External Servo Power Rail",
        "pwr_reset": "Hardware NRST Circuit",
        "clock_source": "72 MHz PLL (Timer Clock = 72 MHz)",
        "clock_timing": "50 Hz PWM Frequency (20 ms Period, ARR=19999, PSC=71)",
        "pin_details": [
            "PA1: TIM2_CH2 PWM Control Output (1.0ms - 2.0ms pulse width)",
            "Common GND: MCU Ground tied to External 5V Servo Ground",
            "PA13/PA14: SWD Programming Interface"
        ],
        "internal_modules": [
            "Timer TIM2 Channel 2 PWM Generator",
            "Compare Register CCR2: 1000 (0°), 1500 (90°), 2000 (180°)"
        ],
        "periph_list": [
            "TowerPro SG90 9g Micro Servo Motor",
            "External 5V 2A Regulated Power Supply",
            "Smoothing Electrolytic Capacitor (100uF on Servo VCC)"
        ],
        "conn_specs": [
            "PA1 (TIM2_CH2) -> Orange/Yellow Servo Control Lead",
            "External +5V -> Red Servo Power Wire",
            "External GND -> Brown Servo Ground Wire & MCU GND"
        ]
    },
    {
        "task_id": "TASK10C",
        "path": "STM32/CAT10/TASK10C/circuit.png",
        "title": "Dual-Channel Complementary PWM Motor Driver on TIM2 CH3 & CH4",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Architecture",
        "pwr_vcc": "+3.3V Logic Rail & +12V DC Motor Power Rail",
        "pwr_reset": "Hardware NRST Reset Network",
        "clock_source": "72 MHz PLL Clock Source",
        "clock_timing": "10 kHz High-Frequency Motor PWM (Silent Drive)",
        "pin_details": [
            "PA2: TIM2_CH3 PWM Output (Left Motor Channel)",
            "PA3: TIM2_CH4 PWM Output (Right Motor Channel)",
            "PB0, PB1: Motor Direction Logic Control Pins"
        ],
        "internal_modules": [
            "Timer TIM2 Multi-Channel Output Compare",
            "Differential Steering Velocity Controller"
        ],
        "periph_list": [
            "L298N Dual Full-Bridge Motor Driver Module",
            "2x 12V High-Torque Geared DC Motors",
            "External 12V 3A Li-ion Battery Pack"
        ],
        "conn_specs": [
            "PA2 & PA3 -> L298N Enable Pins ENA & ENB",
            "PB0 & PB1 -> L298N Direction Inputs IN1..IN4",
            "L298N OUT1..OUT4 -> Left and Right Motor Terminals"
        ]
    },
    {
        "task_id": "TASK11A",
        "path": "STM32/CAT11/TASK11A/circuit.png",
        "title": "USART2 Asynchronous Serial Communication & Telemetry Link",
        "mcu_name": "STM32F401RET6 (Nucleo-64)",
        "mcu_arch": "ARM Cortex-M4F 32-bit Core",
        "pwr_vcc": "+3.3V DC System Operating Power",
        "pwr_reset": "Onboard NRST Button",
        "clock_source": "84 MHz PLL Core Frequency",
        "clock_timing": "115200 Baud Standard Serial Bit Clock",
        "pin_details": [
            "PA2: USART2_TX (Connected to ST-LINK Virtual COM Port)",
            "PA3: USART2_RX (Connected to ST-LINK Virtual COM Port)",
            "PA5: Heartbeat Diagnostic LED (LD2)"
        ],
        "internal_modules": [
            "Universal Synchronous Asynchronous Receiver Transmitter (USART2)",
            "Circular Transmit Buffer & Standard I/O Formatter"
        ],
        "periph_list": [
            "Onboard ST-LINK/V2-1 USB Virtual COM Port Bridge",
            "PC Terminal Console (PuTTY / TeraTerm / Serial Monitor)",
            "High-Speed USB Host Cable"
        ],
        "conn_specs": [
            "PA2 (TX) -> ST-LINK VCP RX (Internal PCB Trace)",
            "PA3 (RX) -> ST-LINK VCP TX (Internal PCB Trace)",
            "ST-LINK USB -> PC USB Port (Appears as /dev/ttyACM0 or COMx)"
        ]
    },
    {
        "task_id": "TASK11B",
        "path": "STM32/CAT11/TASK11B/circuit.png",
        "title": "Interrupt-Driven Interactive Command Line Shell via USART2",
        "mcu_name": "STM32F401RET6 (Nucleo-64)",
        "mcu_arch": "ARM Cortex-M4F 32-bit RISC Core",
        "pwr_vcc": "+3.3V DC System Power",
        "pwr_reset": "Hardware NRST Reset Button",
        "clock_source": "84 MHz PLL Core Frequency",
        "clock_timing": "Zero-Overhead Asynchronous RX Interrupt (RXNE)",
        "pin_details": [
            "PA2: USART2_TX Output Line",
            "PA3: USART2_RX Input Line with RXNE Interrupt",
            "PA5: Controlled Actuator LED (LD2)"
        ],
        "internal_modules": [
            "HAL_UART_Receive_IT() Non-Blocking State Machine",
            "HAL_UART_RxCpltCallback Ring Buffer Parser"
        ],
        "periph_list": [
            "ST-LINK VCP USB Interface",
            "Host PC Interactive CLI Terminal",
            "Green Actuator LED LD2 on PA5"
        ],
        "conn_specs": [
            "PA2 & PA3 -> ST-LINK VCP Serial Transceiver",
            "PC Terminal -> Sends ASCII Commands ('ON', 'OFF', 'STATUS')",
            "MCU -> Echoes Characters & Executes State Changes"
        ]
    },
    {
        "task_id": "TASK12A",
        "path": "STM32/CAT12/TASK12A/circuit.png",
        "title": "I2C1 Hardware Master Bus Initialization & Peripheral Device Scanner",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Architecture",
        "pwr_vcc": "+3.3V DC Regulated Sensor & MCU Bus",
        "pwr_reset": "Hardware Power-On Reset Circuit",
        "clock_source": "72 MHz PLL Core Clock",
        "clock_timing": "100 kHz Standard Mode I2C Clock (SCL)",
        "pin_details": [
            "PB6: I2C1_SCL (Serial Clock Line with 4.7k Pull-up)",
            "PB7: I2C1_SDA (Serial Data Line with 4.7k Pull-up)",
            "PA9/PA10: USART1 Telemetry Console for Scan Output"
        ],
        "internal_modules": [
            "I2C1 Master Peripheral Engine (Open-Drain Configuration)",
            "HAL_I2C_IsDeviceReady() Address Scanner (0x01 to 0x7F)"
        ],
        "periph_list": [
            "Bosch Sensortec BME280 Sensor Breakout (7-bit Addr: 0x76)",
            "2x 4.7k Ohm Metal Film Pull-Up Resistors to 3.3V",
            "ST-LINK V2 SWD Debugger Link"
        ],
        "conn_specs": [
            "PB6 (SCL) -> BME280 SCL & 4.7k Resistor to +3.3V",
            "PB7 (SDA) -> BME280 SDA & 4.7k Resistor to +3.3V",
            "BME280 VCC -> +3.3V, GND -> Common GND"
        ]
    },
    {
        "task_id": "TASK12B",
        "path": "STM32/CAT12/TASK12B/circuit.png",
        "title": "Bosch Sensortec BME280 Chip ID & Factory Calibration Retrieval",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Architecture",
        "pwr_vcc": "+3.3V DC Operating Rail",
        "pwr_reset": "Standard Hardware Reset Network",
        "clock_source": "72 MHz PLL System Clock",
        "clock_timing": "100 kHz I2C Memory Read Protocol",
        "pin_details": [
            "PB6: I2C1_SCL Serial Clock",
            "PB7: I2C1_SDA Serial Data",
            "PA9: USART1_TX Calibration Telemetry Output"
        ],
        "internal_modules": [
            "HAL_I2C_Mem_Read() Direct Register Access Driver",
            "BME280 Factory NVM Calibration Register Map (0x88..0xA1, 0xE1..0xE7)"
        ],
        "periph_list": [
            "Bosch BME280 Precision Environmental Sensor",
            "2x 4.7k Ohm Pull-Up Resistors",
            "USB to UART Serial Cable for PC Debug Logging"
        ],
        "conn_specs": [
            "PB6 -> BME280 SCL (Pin 3)",
            "PB7 -> BME280 SDA (Pin 4)",
            "BME280 Chip ID Register (0xD0) Reads 0x60 (Verification)"
        ]
    },
    {
        "task_id": "TASK12C",
        "path": "STM32/CAT12/TASK12C/circuit.png",
        "title": "Tri-Parameter Environmental Telemetry Acquisition (Temp, Press, Hum)",
        "mcu_name": "STM32F103C8T6 (Blue Pill)",
        "mcu_arch": "ARM Cortex-M3 32-bit Architecture",
        "pwr_vcc": "+3.3V DC Sensor & Core Rail",
        "pwr_reset": "Hardware NRST Network",
        "clock_source": "72 MHz PLL Clock Source",
        "clock_timing": "1 Hz Continuous Sensor Sampling Cycle",
        "pin_details": [
            "PB6: I2C1_SCL Clock Line",
            "PB7: I2C1_SDA Data Line",
            "PA9: USART1_TX Physical Value Telemetry Stream"
        ],
        "internal_modules": [
            "Official Bosch Sensortec BME280 Sensor Driver API",
            "64-bit Integer & Float Pressure/Temperature Compensation Math"
        ],
        "periph_list": [
            "Bosch BME280 Digital Sensor Module",
            "4.7k Bus Pull-Up Resistors",
            "PC Serial Host Terminal"
        ],
        "conn_specs": [
            "PB6 -> BME280 SCL, PB7 -> BME280 SDA",
            "BME280 SDO -> GND (Sets 7-bit Address to 0x76)",
            "Compensated Telemetry: Temp (°C), Press (hPa), Hum (%RH)"
        ]
    },
    {
        "task_id": "TASK13",
        "path": "STM32/CAT13/TASK13/circuit.png",
        "title": "End-to-End MQTT Telemetry Pipeline to Cloud Broker (broker.emqx.io)",
        "mcu_name": "STM32F103C8T6 + Wemos D1 Mini ESP8266",
        "mcu_arch": "ARM Cortex-M3 Core + Tensilica Xtensa Wi-Fi Modem",
        "pwr_vcc": "+3.3V DC (STM32) & High-Current +3.3V (ESP8266 500mA Peak)",
        "pwr_reset": "Dedicated RC Reset Circuits for both ICs",
        "clock_source": "72 MHz (STM32) & 80 MHz (ESP8266 Wi-Fi Core)",
        "clock_timing": "115200 Baud USART Inter-IC AT Command Bus",
        "pin_details": [
            "PA2 (USART2_TX): Commands to ESP8266 RX",
            "PA3 (USART2_RX): Responses from ESP8266 TX",
            "PB6 / PB7: I2C1 Sensor Bus (BME280)"
        ],
        "internal_modules": [
            "Hayes AT Command State Parser (AT+CWMODE, AT+CIPSTART)",
            "Embedded Lightweight MQTT Packet Serializer (QoS 0)"
        ],
        "periph_list": [
            "Wemos D1 Mini ESP8266 Wi-Fi Transceiver Board",
            "Bosch BME280 Multi-Sensor Module",
            "Dedicated AMS1117-3.3V Voltage Regulator with 470uF Cap"
        ],
        "conn_specs": [
            "STM32 PA2 (TX) -> ESP8266 RX (Pin D4)",
            "STM32 PA3 (RX) -> ESP8266 TX (Pin D3)",
            "ESP8266 Wi-Fi -> Cloud Broker: broker.emqx.io:1883"
        ]
    },
    {
        "task_id": "TASK14",
        "path": "STM32/CAT14/TASK14/circuit.png",
        "title": "Real-Time Node-RED Web UI Telemetry Visualization & Gauges",
        "mcu_name": "STM32F103C8T6 + ESP8266 + Node-RED Host",
        "mcu_arch": "32-bit Distributed IoT Architecture",
        "pwr_vcc": "+3.3V System Rails & 5V USB Gateway Power",
        "pwr_reset": "Synchronized Power-On Reset Network",
        "clock_source": "72 MHz PLL Core & 2.4 GHz 802.11 b/g/n RF",
        "clock_timing": "Sub-Second WebSocket Browser Push Updates",
        "pin_details": [
            "PA2 / PA3: USART2 Gateway Communication Lines",
            "PB6 / PB7: I2C1 Sensor Acquisition Interface",
            "TCP/IP Port 1883: Cloud MQTT Ingest / Port 1880: Node-RED Dashboard"
        ],
        "internal_modules": [
            "Embedded JSON Telemetry Serializer",
            "Node-RED Dashboard 2.0 Web Engine & Real-Time Flow Pipeline"
        ],
        "periph_list": [
            "Wemos D1 Mini Wi-Fi Gateway",
            "Node-RED Cloud / Local SCADA Server",
            "Client Web Browser (Desktop / Mobile Tablet UI)"
        ],
        "conn_specs": [
            "STM32 -> JSON Telemetry -> ESP8266 -> Wi-Fi AP",
            "Wi-Fi AP -> MQTT Broker (broker.emqx.io:1883)",
            "Broker -> Node-RED MQTT Input -> Dashboard 2.0 Gauges & Charts"
        ]
    },
    {
        "task_id": "TASK15",
        "path": "STM32/CAT15/TASK15/circuit.png",
        "title": "Automated Weather Monitoring & School Conduction/Holiday Advisory System",
        "mcu_name": "STM32F401RET6 (Nucleo-64) + ESP8266 + Node-RED",
        "mcu_arch": "ARM Cortex-M4F Capstone Edge Gateway & Decision Engine",
        "pwr_vcc": "+3.3V Logic, +5V System Rail & Isolated Sensor Power",
        "pwr_reset": "Hardware NRST System Reset",
        "clock_source": "84 MHz PLL Core & 2.4 GHz RF Carrier",
        "clock_timing": "Real-Time Meteorological Monitoring (1 Hz Continuous Cycle)",
        "pin_details": [
            "PB8: I2C1_SCL Clock Line to Bosch BME280",
            "PB9: I2C1_SDA Data Line to Bosch BME280",
            "PA2 / PA3: USART2 Gateway TX/RX to ESP8266 Wi-Fi Module",
            "PA5: Visual Hardware Warning Status Indicator LED (LD2)"
        ],
        "internal_modules": [
            "Tri-Parameter Meteorological Sensor Acquisition Engine",
            "Civic Safety Rule-Based Decision Classifier in Node-RED"
        ],
        "periph_list": [
            "Bosch BME280 Temperature, Humidity & Barometric Pressure Sensor",
            "Wemos D1 Mini ESP8266 Gateway Transceiver",
            "Node-RED Dashboard 2.0 Real-Time Civic Advisory Web Portal"
        ],
        "conn_specs": [
            "BME280 (I2C1) -> STM32F401RE (PB8/PB9) Sensors",
            "STM32F401RE (PA2/PA3) -> ESP8266 Gateway -> MQTT Topic 'college/weather/bme280'",
            "Node-RED Engine -> Evaluates Pressure (<1000 hPa) & Humidity (>85% RH)",
            "Dashboard UI -> Displays 'CONDUCT SCHOOL' (Normal) vs 'DECLARE HOLIDAY' (Alert)"
        ]
    }
]

def render_all_schematics():
    for idx, meta in enumerate(SCHEMATIC_SPECS):
        out_path = meta["path"].replace("/", os.sep)
        fig, ax = plt.subplots(figsize=(15, 9), dpi=200)
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 9)
        ax.axis('off')

        bg_color = '#FFFFFF'
        border_color = '#0F172A'
        title_banner = '#1E293B'
        mcu_border = '#1E3A8A'
        mcu_bg = '#F8FAFC'
        pwr_border = '#DC2626'
        pwr_bg = '#FEF2F2'
        clk_border = '#059669'
        clk_bg = '#F0FDF4'
        periph_border = '#7C3AED'
        periph_bg = '#FAF5FF'
        wire_color = '#0284C7'
        text_main = '#0F172A'
        text_muted = '#475569'

        fig.patch.set_facecolor(bg_color)

        frame = patches.Rectangle((0.3, 0.3), 14.4, 8.4, linewidth=2, edgecolor=border_color, facecolor=bg_color, zorder=1)
        ax.add_patch(frame)
        inner_frame = patches.Rectangle((0.35, 0.35), 14.3, 8.3, linewidth=0.8, edgecolor='#CBD5E1', facecolor='none', zorder=1)
        ax.add_patch(inner_frame)

        header = patches.Rectangle((0.3, 7.8), 14.4, 0.9, facecolor=title_banner, zorder=2)
        ax.add_patch(header)
        ax.text(7.5, 8.35, 'SHIV NADAR UNIVERSITY CHENNAI — DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING', 
                color='#FFFFFF', fontsize=11, fontweight='bold', ha='center', va='center', zorder=3)
        sub_title = meta['task_id'] + ': ' + meta['title'] + ' | 25CS2741 (FIoT) | Student: P Deepak (25011102072)'
        ax.text(7.5, 8.0, sub_title, color='#38BDF8', fontsize=10, fontweight='bold', ha='center', va='center', zorder=3)

        # 1. Power Supply Block
        pwr_box = patches.FancyBboxPatch((0.6, 5.6), 3.2, 1.9, boxstyle='round,pad=0.1', 
                                         edgecolor=pwr_border, facecolor=pwr_bg, linewidth=1.5, zorder=2)
        ax.add_patch(pwr_box)
        ax.text(2.2, 7.15, 'POWER SUPPLY & RESET', color=pwr_border, fontsize=10, fontweight='bold', ha='center', zorder=3)
        pwr_text = f"VCC: {meta['pwr_vcc']}\nGND: 0V Common Reference\nDecoupling: 100nF Cer + 10uF Tant\nReset: {meta['pwr_reset']}"
        ax.text(2.2, 6.35, pwr_text, color=text_main, fontsize=8.2, ha='center', va='center', zorder=3)

        # 2. Clock & Oscillator Block
        clk_box = patches.FancyBboxPatch((0.6, 3.2), 3.2, 2.0, boxstyle='round,pad=0.1', 
                                         edgecolor=clk_border, facecolor=clk_bg, linewidth=1.5, zorder=2)
        ax.add_patch(clk_box)
        ax.text(2.2, 4.85, 'CLOCK & TIMING SOURCE', color=clk_border, fontsize=10, fontweight='bold', ha='center', zorder=3)
        clk_text = f"Source: {meta['clock_source']}\nLoad Capacitors: 2x 22pF\nTimebase: {meta['clock_timing']}\nDrift Stability: ±20 ppm"
        ax.text(2.2, 4.0, clk_text, color=text_main, fontsize=8.2, ha='center', va='center', zorder=3)

        # 3. Microcontroller Block (Center)
        mcu_box = patches.FancyBboxPatch((4.3, 2.2), 5.3, 5.3, boxstyle='round,pad=0.15', 
                                         edgecolor=mcu_border, facecolor=mcu_bg, linewidth=2.0, zorder=2)
        ax.add_patch(mcu_box)
        ax.text(6.95, 7.15, meta['mcu_name'], color=mcu_border, fontsize=12, fontweight='bold', ha='center', zorder=3)
        ax.text(6.95, 6.8, meta['mcu_arch'], color=text_muted, fontsize=8, fontstyle='italic', ha='center', zorder=3)

        ax.text(4.6, 6.35, 'ACTIVE HARDWARE INTERFACES:', color=text_main, fontsize=9, fontweight='bold', zorder=3)
        pins = meta['pin_details']
        y_p = 5.95
        for p in pins:
            ax.text(4.7, y_p, f"• {p}", color=mcu_border, fontsize=7.8, zorder=3)
            y_p -= 0.35

        ax.text(4.6, y_p - 0.1, 'INTERNAL HARDWARE MODULES:', color=text_main, fontsize=9, fontweight='bold', zorder=3)
        modules = meta['internal_modules']
        for m in modules:
            ax.text(4.7, y_p - 0.45, f"• {m}", color=clk_border, fontsize=7.8, zorder=3)
            y_p -= 0.35

        # 4. External Peripheral Block (Right)
        periph_box = patches.FancyBboxPatch((10.1, 2.2), 4.3, 5.3, boxstyle='round,pad=0.15', 
                                           edgecolor=periph_border, facecolor=periph_bg, linewidth=2.0, zorder=2)
        ax.add_patch(periph_box)
        ax.text(12.25, 7.15, 'EXTERNAL PERIPHERAL / ACTUATOR', color=periph_border, fontsize=10.5, fontweight='bold', ha='center', zorder=3)
        
        periph_items = meta['periph_list']
        py = 6.6
        for item in periph_items:
            ax.text(10.35, py, f"▪ {item}", color=text_main, fontsize=8.2, zorder=3)
            py -= 0.4

        ax.text(10.35, py - 0.1, 'PHYSICAL INTERCONNECTION SPEC:', color=text_main, fontsize=9, fontweight='bold', zorder=3)
        specs = meta['conn_specs']
        for s in specs:
            ax.text(10.35, py - 0.45, f"→ {s}", color=periph_border, fontsize=7.8, zorder=3)
            py -= 0.35

        # Connections
        ax.annotate('', xy=(4.3, 6.5), xytext=(3.8, 6.5),
                    arrowprops=dict(arrowstyle='->', color=pwr_border, lw=2, mutation_scale=15), zorder=4)
        ax.text(4.05, 6.7, 'VCC', color=pwr_border, fontsize=8, fontweight='bold', ha='center', zorder=4)

        ax.annotate('', xy=(4.3, 4.2), xytext=(3.8, 4.2),
                    arrowprops=dict(arrowstyle='->', color=clk_border, lw=2, mutation_scale=15), zorder=4)
        ax.text(4.05, 4.4, 'OSC_IN', color=clk_border, fontsize=8, fontweight='bold', ha='center', zorder=4)

        ax.annotate('', xy=(10.1, 5.2), xytext=(9.6, 5.2),
                    arrowprops=dict(arrowstyle='<->', color=wire_color, lw=2.5, mutation_scale=18), zorder=4)
        ax.text(9.85, 5.5, 'BUS LINES', color=wire_color, fontsize=8, fontweight='bold', ha='center', zorder=4)

        ax.annotate('', xy=(12.25, 2.2), xytext=(6.95, 2.2),
                    arrowprops=dict(arrowstyle='-', color='#64748B', lw=1.5, ls='--'), zorder=4)
        ax.annotate('', xy=(6.95, 2.2), xytext=(2.2, 3.2),
                    arrowprops=dict(arrowstyle='-', color='#64748B', lw=1.5, ls='--'), zorder=4)
        ax.text(6.95, 1.85, 'COMMON GROUND BUS (0V POTENTIAL REFERENCE)', color='#64748B', fontsize=8, fontweight='bold', ha='center', zorder=4)

        # Title Block
        tb = patches.Rectangle((9.4, 0.4), 5.2, 1.2, edgecolor='#94A3B8', facecolor='#F1F5F9', linewidth=1.0, zorder=2)
        ax.add_patch(tb)
        ax.text(9.6, 1.35, f"DWG: 25CS2741-{meta['task_id']}-SCHEMATIC", color=text_main, fontsize=8, fontweight='bold', zorder=3)
        ax.text(9.6, 1.05, f"TITLE: {meta['title'][:32]}", color=text_main, fontsize=7.5, zorder=3)
        ax.text(9.6, 0.75, "DESIGNER: P Deepak | REG: 25011102072", color=text_muted, fontsize=7.5, zorder=3)
        ax.text(9.6, 0.5, "REV: 2.0 (Engineering Verified) | SNU Chennai", color=text_muted, fontsize=7, zorder=3)

        plt.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=200, facecolor=bg_color)
        plt.close()
        print(f"[{idx+1}/{len(SCHEMATIC_SPECS)}] Rendered {out_path}")

    # Also render root architecture schematic
    render_root_architecture("circuit.png")

def render_root_architecture(output_path):
    fig, ax = plt.subplots(figsize=(15, 9), dpi=200)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis('off')

    bg_color = '#FFFFFF'
    border_color = '#0F172A'
    title_banner = '#1E293B'

    fig.patch.set_facecolor(bg_color)
    frame = patches.Rectangle((0.3, 0.3), 14.4, 8.4, linewidth=2, edgecolor=border_color, facecolor=bg_color, zorder=1)
    ax.add_patch(frame)
    inner_frame = patches.Rectangle((0.35, 0.35), 14.3, 8.3, linewidth=0.8, edgecolor='#CBD5E1', facecolor='none', zorder=1)
    ax.add_patch(inner_frame)

    header = patches.Rectangle((0.3, 7.8), 14.4, 0.9, facecolor=title_banner, zorder=2)
    ax.add_patch(header)
    ax.text(7.5, 8.35, 'FOUNDATIONS OF IoT (25CS2741) — LABORATORY SYSTEM ARCHITECTURE', 
            color='#FFFFFF', fontsize=12, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(7.5, 8.0, 'Student: P Deepak | Register Number: 25011102072 | Shiv Nadar University Chennai', 
            color='#38BDF8', fontsize=10, fontweight='bold', ha='center', va='center', zorder=3)

    # 8051 Platform Box (Left)
    box_8051 = patches.FancyBboxPatch((0.8, 1.8), 6.3, 5.7, boxstyle='round,pad=0.15', 
                                      edgecolor='#059669', facecolor='#F0FDF4', linewidth=2.0, zorder=2)
    ax.add_patch(box_8051)
    ax.text(3.95, 7.15, '8051 HARDWARE PLATFORM (CAT 2 - CAT 7)', color='#059669', fontsize=11, fontweight='bold', ha='center', zorder=3)
    t_8051 = (
        "• Core Processor: AT89C51 / AT89S52 @ 11.0592 MHz\n"
        "• Toolchain: Keil C51 Embedded Compiler & Simulator\n"
        "• Architecture: 8-bit CISC with Harvard Memory Architecture\n"
        "• Direct Special Function Register (SFR) Control\n\n"
        "Laboratory Implementations:\n"
        "  - CAT 2: GPIO Port Programming & Calibrated Delay Loops\n"
        "  - CAT 3: Tactile Switch Debouncing & Bitwise Input Reading\n"
        "  - CAT 4: Hardware Timer 0 Mode 1 (16-bit) 1 kHz Waves\n"
        "  - CAT 5: External Interrupt 0 (INT0) Preemptive E-Stop\n"
        "  - CAT 5B: Multiplexed 7-Segment Displays (POV Refresh)\n"
        "  - CAT 5C: HD44780 16x2 Alphanumeric Parallel LCD Driver\n"
        "  - CAT 6: 4x4 Matrix Keypad Scanning & Passcode Security\n"
        "  - CAT 7: Stepper Motor (ULN2003) & DC Motor (L293D PWM)"
    )
    ax.text(1.1, 4.4, t_8051, color='#0F172A', fontsize=8.8, va='center', zorder=3)

    # STM32 Platform Box (Right)
    box_stm32 = patches.FancyBboxPatch((7.9, 1.8), 6.3, 5.7, boxstyle='round,pad=0.15', 
                                       edgecolor='#1D4ED8', facecolor='#EFF6FF', linewidth=2.0, zorder=2)
    ax.add_patch(box_stm32)
    ax.text(11.05, 7.15, 'STM32 ARM CORTEX PLATFORM (CAT 8 - CAT 15)', color='#1D4ED8', fontsize=11, fontweight='bold', ha='center', zorder=3)
    t_stm32 = (
        "• Processors: STM32F103C8T6 (72MHz) & STM32F401RET6 (84MHz)\n"
        "• Toolchain: STM32CubeMX HAL + Keil MDK-ARM v5\n"
        "• Architecture: 32-bit ARM Cortex-M3/M4F with CMSIS\n"
        "• Multi-Channel Peripherals, Timers, DMA & Advanced Buses\n\n"
        "Laboratory Implementations:\n"
        "  - CAT 8: GPIO Bring-up, Software Debouncing & Ring Chasers\n"
        "  - CAT 9: Nucleo-F401RE High-Speed Heartbeat & EXTI13 IRQ\n"
        "  - CAT 10: Hardware PWM Breathing LED, Servo & Dual DC\n"
        "  - CAT 11: USART2 Asynchronous Telemetry & Interactive CLI\n"
        "  - CAT 12: Hardware I2C Master & Bosch BME280 Driver\n"
        "  - CAT 13: Wi-Fi ESP8266 Modem & Cloud MQTT Ingestion\n"
        "  - CAT 14: Real-Time Node-RED Dashboard 2.0 SCADA Telemetry\n"
        "  - CAT 15: Capstone Severe Weather Civic Advisory Engine"
    )
    ax.text(8.2, 4.4, t_stm32, color='#0F172A', fontsize=8.8, va='center', zorder=3)

    # Central Data Flow Arrow
    ax.annotate('', xy=(7.9, 4.6), xytext=(7.1, 4.6),
                arrowprops=dict(arrowstyle='<->', color='#D97706', lw=3, mutation_scale=20), zorder=4)
    ax.text(7.5, 4.9, 'PORTING & EVOLUTION', color='#B45309', fontsize=8, fontweight='bold', ha='center', zorder=4)

    # Footer Title Block
    tb = patches.Rectangle((9.4, 0.4), 5.2, 1.2, edgecolor='#94A3B8', facecolor='#F1F5F9', linewidth=1.0, zorder=2)
    ax.add_patch(tb)
    ax.text(9.6, 1.35, "DWG: 25CS2741-MASTER-ARCHITECTURE", color='#0F172A', fontsize=8, fontweight='bold', zorder=3)
    ax.text(9.6, 1.05, "TITLE: Foundations of IoT Dual-Platform Framework", color='#0F172A', fontsize=7.5, zorder=3)
    ax.text(9.6, 0.75, "DESIGNER: P Deepak | REG: 25011102072", color='#475569', fontsize=7.5, zorder=3)
    ax.text(9.6, 0.5, "REV: 2.0 (Engineering Verified) | SNU Chennai", color='#475569', fontsize=7, zorder=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, facecolor=bg_color)
    plt.close()
    print(f"Rendered Master Architecture: {output_path}")

if __name__ == "__main__":
    render_all_schematics()
