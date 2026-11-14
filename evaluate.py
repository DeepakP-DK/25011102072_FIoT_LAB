import os
import sys
import re

EXPECTED_TASKS_8051 = [
    "8051/CAT2/TASK2A",
    "8051/CAT2/TASK2B",
    "8051/CAT2/TASK2C",
    "8051/CAT3/TASK3A",
    "8051/CAT3/TASK3B",
    "8051/CAT3/TASK3C",
    "8051/CAT3/TASK3D",
    "8051/CAT4/TASK4A",
    "8051/CAT4/TASK4B",
    "8051/CAT5/TASK5A",
    "8051/CAT5/TASK5B/TASK5B.1",
    "8051/CAT5/TASK5B/TASK5B.2",
    "8051/CAT5/TASK5B/TASK5B.3",
    "8051/CAT5/TASK5C",
    "8051/CAT6/TASK6A",
    "8051/CAT6/TASK6B",
    "8051/CAT7/TASK7A",
    "8051/CAT7/TASK7B",
    "8051/CAT7/TASK7C",
]

EXPECTED_TASKS_STM32 = [
    "STM32/CAT8/TASK8A",
    "STM32/CAT8/TASK8B",
    "STM32/CAT8/TASK8C",
    "STM32/CAT9/TASK9A",
    "STM32/CAT9/TASK9B",
    "STM32/CAT10/TASK10A",
    "STM32/CAT10/TASK10B",
    "STM32/CAT10/TASK10C",
    "STM32/CAT11/TASK11A",
    "STM32/CAT11/TASK11B",
    "STM32/CAT12/TASK12A",
    "STM32/CAT12/TASK12B",
    "STM32/CAT12/TASK12C",
    "STM32/CAT13/TASK13",
    "STM32/CAT14/TASK14",
    "STM32/CAT15/TASK15",
]

ALL_EXPECTED = EXPECTED_TASKS_8051 + EXPECTED_TASKS_STM32

def check_readme(path):
    if not os.path.exists(path):
        return False, "Missing README.md"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        required_headers = [
            "EXPERIMENT DETAILS",
            "EXP:",
            "DATE:",
            "NAME OF EXP:",
            "HARDWARE SETUP / PLATFORM:",
            "Circuit Diagram",
            "Core Logic / Pseudocode / Code Base",
            "Inference"
        ]
        for h in required_headers:
            if h.lower() not in content.lower():
                return False, f"README missing section '{h}'"
        
        if "circuit.png" not in content:
            return False, "README missing circuit.png reference"
            
        return True, "README valid"
    except Exception as e:
        return False, str(e)

def evaluate(repo_root="."):
    total_checks = 0
    passed_checks = 0
    tasks_passed = 0
    tasks_failed = 0
    
    print("=" * 60)
    print("   FOUNDATIONS OF IoT (25CS2741) EVALUATION REPORT")
    print("=" * 60)
    
    # Check root files
    root_readme = os.path.join(repo_root, "README.md")
    root_circuit = os.path.join(repo_root, "circuit.png")
    root_gitignore = os.path.join(repo_root, ".gitignore")
    
    print("\n[ROOT DIRECTORY CHECKS]")
    for name, p in [("Root README.md", root_readme), ("Root circuit.png", root_circuit), (".gitignore", root_gitignore)]:
        total_checks += 1
        if os.path.exists(p) and os.path.getsize(p) > 0:
            passed_checks += 1
            print(f"  [PASS] {name} present")
        else:
            print(f"  [FAIL] {name} missing or empty")

    results = []
    
    for task_rel in ALL_EXPECTED:
        task_dir = os.path.join(repo_root, task_rel.replace("/", os.sep))
        platform = "8051" if "8051" in task_rel else "STM32"
        task_ok = True
        task_messages = []
        
        if not os.path.exists(task_dir):
            tasks_failed += 1
            print(f"\n[FAIL] {task_rel}: Directory not found!")
            continue
            
        # 1. README.md check
        readme_path = os.path.join(task_dir, "README.md")
        total_checks += 1
        rm_ok, rm_msg = check_readme(readme_path)
        if rm_ok:
            passed_checks += 1
        else:
            task_ok = False
            task_messages.append(rm_msg)
            
        # 2. circuit.png check
        circuit_path = os.path.join(task_dir, "circuit.png")
        total_checks += 1
        if os.path.exists(circuit_path) and os.path.getsize(circuit_path) > 1000:
            passed_checks += 1
        else:
            task_ok = False
            task_messages.append("circuit.png missing or too small")
            
        if platform == "8051":
            # 3. Keil project (*.uvproj or *.uvprojx)
            total_checks += 1
            uvproj_found = any(f.endswith(".uvproj") or f.endswith(".uvprojx") for f in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, f)))
            if uvproj_found:
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing Keil .uvproj/.uvprojx")
                
            # 4. Source code (*.c)
            total_checks += 1
            c_found = any(f.endswith(".c") for f in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, f)))
            if c_found:
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing C source file (*.c)")
                
            # 5. Startup assembly (STARTUP.A51)
            total_checks += 1
            a51_path = os.path.join(task_dir, "STARTUP.A51")
            if os.path.exists(a51_path):
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing STARTUP.A51")
                
            # 6. Objects/*.hex
            total_checks += 1
            obj_dir = os.path.join(task_dir, "Objects")
            hex_found = False
            if os.path.exists(obj_dir):
                hex_found = any(f.endswith(".hex") for f in os.listdir(obj_dir) if os.path.isfile(os.path.join(obj_dir, f)))
            if hex_found:
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing Objects/*.hex")
                
        else: # STM32
            # 3. *.ioc
            total_checks += 1
            ioc_found = any(f.endswith(".ioc") for f in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, f)))
            if ioc_found:
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing *.ioc CubeMX file")
                
            # 4. .mxproject
            total_checks += 1
            mx_path = os.path.join(task_dir, ".mxproject")
            if os.path.exists(mx_path):
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing .mxproject")
                
            # 5. Core/Src/main.c
            total_checks += 1
            main_c_path = os.path.join(task_dir, "Core", "Src", "main.c")
            if os.path.exists(main_c_path):
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing Core/Src/main.c")
                
            # 6. Drivers/
            total_checks += 1
            drivers_path = os.path.join(task_dir, "Drivers")
            if os.path.exists(drivers_path) and os.path.isdir(drivers_path):
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing Drivers/ folder")
                
            # 7. MDK-ARM/*.uvprojx
            total_checks += 1
            mdk_dir = os.path.join(task_dir, "MDK-ARM")
            uvprojx_found = False
            if os.path.exists(mdk_dir):
                uvprojx_found = any(f.endswith(".uvprojx") for f in os.listdir(mdk_dir) if os.path.isfile(os.path.join(mdk_dir, f)))
            if uvprojx_found:
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing MDK-ARM/*.uvprojx")
                
            # 8. MDK-ARM/startup_*.s
            total_checks += 1
            startup_s_found = False
            if os.path.exists(mdk_dir):
                startup_s_found = any(f.startswith("startup_") and f.endswith(".s") for f in os.listdir(mdk_dir) if os.path.isfile(os.path.join(mdk_dir, f)))
            if startup_s_found:
                passed_checks += 1
            else:
                task_ok = False
                task_messages.append("Missing MDK-ARM/startup_*.s")
                
        if task_ok:
            tasks_passed += 1
            results.append((task_rel, "PASS", []))
        else:
            tasks_failed += 1
            results.append((task_rel, "FAIL", task_messages))

    print("\n" + "=" * 60)
    print("                  EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Tasks Discovered : {len(ALL_EXPECTED)}")
    print(f"Tasks Passed     : {tasks_passed} / {len(ALL_EXPECTED)}")
    print(f"Tasks Failed     : {tasks_failed}")
    print(f"File Checks      : {passed_checks} / {total_checks}")
    print("-" * 60)
    
    if tasks_failed == 0 and passed_checks == total_checks:
        print("OVERALL STATUS   : PASSED [100% PERFECT]")
    else:
        print("OVERALL STATUS   : FAILED")
        print("\nFailures:")
        for task, status, msgs in results:
            if status == "FAIL":
                print(f"  {task}: {', '.join(msgs)}")
                
    print("=" * 60)
    return tasks_failed == 0

if __name__ == "__main__":
    success = evaluate()
    sys.exit(0 if success else 1)
