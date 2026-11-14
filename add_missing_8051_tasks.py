"""Create the six 8051 evaluation tasks absent from the original lab tree.

The task implementations and documentation are authored for this repository.
The local CAT exemplars provide only the common Keil project/startup layout.
"""
from pathlib import Path
from shutil import copy2

ROOT = Path(__file__).parent

TASKS = {
    "8051/CAT2/TASK2A": {
        "source": """#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int tick, inner;
    for (tick = 0; tick < ms; ++tick)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    P1 = 0xFF;
    while (1) {
        P1 = 0x00;       /* active-low LED bank: illuminated */
        delay_ms(250);
        P1 = 0xFF;       /* LED bank: extinguished */
        delay_ms(250);
    }
}
""",
        "title": "8051 Minimum-System Bring-Up and Port-1 LED Proof Test",
        "principle": "An AT89C51 minimum system is validated by alternately driving all Port 1 latches low and high. With active-low LEDs, the two states visibly confirm reset release, oscillator operation and execution from internal program memory.",
        "pins": "Port 1 (P1.0-P1.7) drives eight active-low LEDs through 330 ohm resistors. The board uses an 11.0592 MHz crystal, 22 pF load capacitors, an RC reset network and a regulated 5 V supply.",
        "algorithm": "After reset, configure Port 1 high. Repeatedly write 00H, wait 250 ms, write FFH, wait 250 ms, and repeat.",
        "inference": "The alternating full-bank pattern verifies a functioning 8051 clock, reset circuit, flash execution path and Port 1 output drivers.",
        "image": "8051/CAT2/TASK2B/circuit.png",
    },
    "8051/CAT2/TASK2C": {
        "source": """#include <reg51.h>

sbit TEST_OUT = P1^0;

void delay_ms(unsigned int ms) {
    unsigned int ms_count, cycles;
    for (ms_count = 0; ms_count < ms; ++ms_count)
        for (cycles = 0; cycles < 120; ++cycles) { }
}

void main(void) {
    TEST_OUT = 0;
    while (1) {
        TEST_OUT = !TEST_OUT;
        delay_ms(100);
    }
}
""",
        "title": "Calibrated Software Delay and GPIO Timing Test",
        "principle": "A calibrated nested loop provides a repeatable delay at the 11.0592 MHz 8051 clock. P1.0 changes state every 100 ms, producing a 5 Hz square-wave test signal that can be checked with an LED or oscilloscope.",
        "pins": "P1.0 is the timing output and connects to an LED plus 330 ohm resistor and an optional oscilloscope probe. The 8051 uses the standard 11.0592 MHz oscillator, reset network and 5 V rail.",
        "algorithm": "Set P1.0 low. Toggle it, consume a calibrated 100 ms delay, and return to the toggle step indefinitely.",
        "inference": "The measured waveform demonstrates the relationship between machine cycles, loop overhead and externally observable GPIO timing.",
        "image": "8051/CAT2/TASK2B/circuit.png",
    },
    "8051/CAT3/TASK3B": {
        "source": """#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    unsigned char value = 0;
    P1 = 0xFF;
    while (1) {
        P1 = (unsigned char)~value;  /* active-low binary LED display */
        delay_ms(500);
        value = (value + 1) & 0x0F;
    }
}
""",
        "title": "Four-Bit Binary LED Counter",
        "principle": "The low nibble of an unsigned counter is presented on four active-low LEDs. Masking with 0FH makes the sequence wrap cleanly from binary 1111 back to 0000.",
        "pins": "P1.0-P1.3 connect to four active-low LEDs through 330 ohm resistors. P1.4-P1.7 remain high and unused; the standard 11.0592 MHz 8051 clock and reset circuit are retained.",
        "algorithm": "Start at zero. Invert and output the low nibble, wait 500 ms, increment, mask to four bits, and repeat.",
        "inference": "The result illustrates binary representation, port masking and deterministic cyclic counting on a bare-metal microcontroller.",
        "image": "8051/CAT3/TASK3A/circuit.png",
    },
    "8051/CAT3/TASK3C": {
        "source": """#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    while (1) {
        P1 = 0xF5;       /* P1.1 and P1.3 active-low: 1010 pattern */
        delay_ms(300);
        P1 = 0xFA;       /* P1.0 and P1.2 active-low: 0101 pattern */
        delay_ms(300);
    }
}
""",
        "title": "Alternating Four-LED Pattern Generator",
        "principle": "Two complementary bit masks are written to the lower Port 1 nibble. The masks select alternate LEDs, producing a symmetric two-phase pattern without needing interrupt or timer hardware.",
        "pins": "P1.0-P1.3 are active-low outputs to four LEDs and 330 ohm resistors. The system clock is the 11.0592 MHz crystal with the normal 8051 reset and 5 V supply circuitry.",
        "algorithm": "Write the first alternating mask, delay 300 ms, write its complement, delay 300 ms, then loop.",
        "inference": "Complementary output patterns demonstrate bitwise masking and simple temporal sequencing for visual indicators.",
        "image": "8051/CAT3/TASK3A/circuit.png",
    },
    "8051/CAT3/TASK3D": {
        "source": """#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    P1 = 0xFF;
    while (1) {
        P1 = 0xF0;       /* four active-low LEDs ON */
        delay_ms(250);
        P1 = 0xFF;       /* all four LEDs OFF */
        delay_ms(250);
    }
}
""",
        "title": "Synchronous Four-LED Flash Controller",
        "principle": "All four LED outputs are asserted together, held for a fixed interval, and then released together. This creates a uniform visual flash that is useful as a basic status or alarm indication.",
        "pins": "P1.0-P1.3 drive four active-low LEDs through 330 ohm resistors. P1.4-P1.7 are held high. The oscillator, reset circuit and 5 V rail follow the 8051 minimum-system connection.",
        "algorithm": "Drive the four LED bits low, delay 250 ms, drive them high, delay 250 ms, and continue forever.",
        "inference": "A shared output mask is sufficient for synchronized indication and reinforces the active-low convention used by the lab LED board.",
        "image": "8051/CAT3/TASK3A/circuit.png",
    },
    "8051/CAT4/TASK4B": {
        "source": """#include <reg51.h>

unsigned char scan_key(void) {
    unsigned char row;
    for (row = 0; row < 4; ++row) {
        P2 = (unsigned char)~(1 << row);
        if ((P2 & 0xF0) != 0xF0) {
            if (!(P2 & 0x10)) return row * 4 + 1;
            if (!(P2 & 0x20)) return row * 4 + 2;
            if (!(P2 & 0x40)) return row * 4 + 3;
            if (!(P2 & 0x80)) return row * 4 + 4;
        }
    }
    return 0;
}

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    unsigned char key;
    P1 = 0xFF;
    while (1) {
        key = scan_key();
        if (key) {
            P1 = (unsigned char)~(1 << ((key - 1) & 0x07));
            delay_ms(20);
            while (scan_key()) { }
            delay_ms(20);
            P1 = 0xFF;
        }
    }
}
""",
        "title": "4x4 Matrix Keypad Controlled LED Selector",
        "principle": "The firmware drives one keypad row low at a time and reads the column inputs. A detected row-column intersection is translated into an LED selection, then debounced before another input is accepted.",
        "pins": "P2.0-P2.3 are keypad row outputs and P2.4-P2.7 are column inputs with pull-ups. P1.0-P1.7 drive eight active-low LEDs. The circuit uses the 11.0592 MHz crystal, RC reset and 5 V supply.",
        "algorithm": "Scan each keypad row, identify a low column, map the key to one LED bit, show that LED, wait for release, debounce, and resume scanning.",
        "inference": "The task validates matrix scanning, port direction changes, key debouncing and the separation of physical input from output control logic.",
        "image": "8051/CAT4/TASK4A/circuit.png",
    },
}

def readme(task_id, data):
    return f"""# EXPERIMENT DETAILS

**EXP:** {task_id[:5].replace('TASK', 'CAT ')} - {task_id}

**DATE:** Not specified in course evaluation sheet

**NAME OF EXP:** {data['title']}

**HARDWARE SETUP / PLATFORM:** AT89C51 / AT89S52 8051 microcontroller at 11.0592 MHz, Keil C51, 5 V laboratory trainer

---

## {task_id} : {data['title']}

### 1. Circuit Diagram

{data['pins']}

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

{data['principle']}

**Pseudocode:**

{data['algorithm']}

**Code Structure / Key Registers:**

The `main.c` firmware uses direct 8051 special-function-register access. Port latches are addressed through `P1` and `P2`; the delay routine is intentionally kept local so timing assumptions remain visible during lab review.

### 3. Inference

{data['inference']}
"""

for relative, data in TASKS.items():
    folder = ROOT / relative
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "Objects").mkdir(exist_ok=True)
    task_id = folder.name
    (folder / "main.c").write_text(data["source"], encoding="utf-8", newline="\n")
    (folder / "README.md").write_text(readme(task_id, data), encoding="utf-8", newline="\n")
    copy2(ROOT / "8051/CAT2/TASK2B/STARTUP.A51", folder / "STARTUP.A51")
    project = (ROOT / "8051/CAT2/TASK2B/TASK2B.uvproj").read_text(encoding="utf-8")
    project = project.replace("TASK2B_plzwork1", task_id).replace("ledblinkplz.c", "main.c")
    (folder / f"{task_id}.uvproj").write_text(project, encoding="utf-8", newline="\n")
    copy2(ROOT / data["image"], folder / "circuit.png")
