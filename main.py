"""
Interactive CLI Utility Suite
Includes:
1. Task Manager (with JSON persistence, priorities, and category filtering)
2. Unit Converter (Temperature, Distance, Weight, Digital Storage)
3. Scientific Calculator & Math Utilities (with calculation history)
"""

import json
import math
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

# ANSI Color codes for clean terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def color_text(text: str, color_code: str) -> str:
    """Utility to format text with ANSI colors if supported by terminal."""
    return f"{color_code}{text}{Colors.RESET}"

# ==========================================
# 1. TASK MANAGER MODULE
# ==========================================
class TaskManager:
    TASKS_FILE = "tasks.json"

    def __init__(self):
        self.tasks: List[Dict[str, Any]] = self.load_tasks()

    def load_tasks(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.TASKS_FILE):
            try:
                with open(self.TASKS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_tasks(self):
        with open(self.TASKS_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title: str, category: str = "General", priority: str = "Medium"):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.tasks.append(task)
        self.save_tasks()
        print(color_text(f"\n[+] Task '{title}' added successfully!", Colors.GREEN))

    def view_tasks(self, filter_completed: Optional[bool] = None):
        if not self.tasks:
            print(color_text("\nNo tasks available.", Colors.YELLOW))
            return

        filtered = self.tasks
        if filter_completed is not None:
            filtered = [t for t in self.tasks if t['completed'] == filter_completed]

        if not filtered:
            print(color_text("\nNo matching tasks found.", Colors.YELLOW))
            return

        print("\n" + "=" * 68)
        print(color_text(f"{'ID':<4} {'Status':<10} {'Priority':<10} {'Category':<12} {'Title'}", Colors.BOLD))
        print("=" * 68)
        for t in filtered:
            status = color_text("[X] Done", Colors.GREEN) if t['completed'] else color_text("[ ] Pending", Colors.YELLOW)
            p_color = Colors.RED if t['priority'] == 'High' else (Colors.CYAN if t['priority'] == 'Medium' else Colors.BLUE)
            priority = color_text(t['priority'], p_color)
            print(f"{t['id']:<4} {status:<19} {priority:<19} {t['category']:<12} {t['title']}")
        print("=" * 68)

    def toggle_task(self, task_id: int):
        for t in self.tasks:
            if t['id'] == task_id:
                t['completed'] = not t['completed']
                self.save_tasks()
                status_str = "completed" if t['completed'] else "marked as pending"
                print(color_text(f"\n[+] Task #{task_id} {status_str}.", Colors.GREEN))
                return
        print(color_text(f"\n[-] Task ID #{task_id} not found.", Colors.RED))

    def delete_task(self, task_id: int):
        for i, t in enumerate(self.tasks):
            if t['id'] == task_id:
                removed = self.tasks.pop(i)
                # Re-index remaining task IDs
                for idx, item in enumerate(self.tasks):
                    item['id'] = idx + 1
                self.save_tasks()
                print(color_text(f"\n[+] Task '{removed['title']}' deleted.", Colors.GREEN))
                return
        print(color_text(f"\n[-] Task ID #{task_id} not found.", Colors.RED))


def run_task_manager():
    tm = TaskManager()
    while True:
        print("\n" + color_text("--- TASK MANAGER ---", Colors.HEADER))
        print("1. View All Tasks")
        print("2. Add New Task")
        print("3. Toggle Task Completion")
        print("4. Delete Task")
        print("5. Back to Main Menu")
        
        choice = input(color_text("Select an option (1-5): ", Colors.CYAN)).strip()
        if choice == '1':
            tm.view_tasks()
        elif choice == '2':
            title = input("Enter task title: ").strip()
            if not title:
                print(color_text("Title cannot be empty.", Colors.RED))
                continue
            category = input("Enter category (default: General): ").strip() or "General"
            print("Select Priority: 1) Low  2) Medium  3) High")
            p_choice = input("Choice (1-3): ").strip()
            priority_map = {'1': 'Low', '2': 'Medium', '3': 'High'}
            priority = priority_map.get(p_choice, 'Medium')
            tm.add_task(title, category, priority)
        elif choice == '3':
            tm.view_tasks()
            try:
                tid = int(input("Enter Task ID to toggle: ").strip())
                tm.toggle_task(tid)
            except ValueError:
                print(color_text("Invalid ID number.", Colors.RED))
        elif choice == '4':
            tm.view_tasks()
            try:
                tid = int(input("Enter Task ID to delete: ").strip())
                tm.delete_task(tid)
            except ValueError:
                print(color_text("Invalid ID number.", Colors.RED))
        elif choice == '5':
            break
        else:
            print(color_text("Invalid choice, please try again.", Colors.RED))

# ==========================================
# 2. UNIT CONVERTER MODULE
# ==========================================
def run_unit_converter():
    while True:
        print("\n" + color_text("--- UNIT CONVERTER ---", Colors.HEADER))
        print("1. Temperature (Celsius <-> Fahrenheit <-> Kelvin)")
        print("2. Distance (Meters <-> Kilometers <-> Miles <-> Feet)")
        print("3. Weight (Kilograms <-> Grams <-> Pounds <-> Ounces)")
        print("4. Data Storage (Bytes <-> KB <-> MB <-> GB <-> TB)")
        print("5. Back to Main Menu")

        choice = input(color_text("Select category (1-5): ", Colors.CYAN)).strip()
        
        if choice == '1':
            print("\nTemperature Conversion:")
            print("a) Celsius to Fahrenheit & Kelvin")
            print("b) Fahrenheit to Celsius & Kelvin")
            sub = input("Select option (a/b): ").strip().lower()
            try:
                val = float(input("Enter value: "))
                if sub == 'a':
                    f = (val * 9/5) + 32
                    k = val + 273.15
                    print(color_text(f"\n{val}°C = {f:.2f}°F | {k:.2f}K", Colors.GREEN))
                elif sub == 'b':
                    c = (val - 32) * 5/9
                    k = c + 273.15
                    print(color_text(f"\n{val}°F = {c:.2f}°C | {k:.2f}K", Colors.GREEN))
            except ValueError:
                print(color_text("Invalid input number.", Colors.RED))

        elif choice == '2':
            print("\nDistance Conversion:")
            print("a) Meters -> KM, Miles, Feet")
            print("b) Miles -> KM, Meters, Feet")
            sub = input("Select option (a/b): ").strip().lower()
            try:
                val = float(input("Enter distance: "))
                if sub == 'a':
                    km = val / 1000
                    mi = val * 0.000621371
                    ft = val * 3.28084
                    print(color_text(f"\n{val} meters = {km:.3f} km | {mi:.3f} miles | {ft:.2f} feet", Colors.GREEN))
                elif sub == 'b':
                    km = val * 1.60934
                    m = km * 1000
                    ft = val * 5280
                    print(color_text(f"\n{val} miles = {km:.3f} km | {m:.1f} meters | {ft:.1f} feet", Colors.GREEN))
            except ValueError:
                print(color_text("Invalid input number.", Colors.RED))

        elif choice == '3':
            print("\nWeight Conversion:")
            print("a) Kilograms -> Grams, Pounds, Ounces")
            print("b) Pounds -> KG, Grams, Ounces")
            sub = input("Select option (a/b): ").strip().lower()
            try:
                val = float(input("Enter weight: "))
                if sub == 'a':
                    g = val * 1000
                    lbs = val * 2.20462
                    oz = val * 35.274
                    print(color_text(f"\n{val} kg = {g:.1f} g | {lbs:.2f} lbs | {oz:.2f} oz", Colors.GREEN))
                elif sub == 'b':
                    kg = val / 2.20462
                    g = kg * 1000
                    oz = val * 16
                    print(color_text(f"\n{val} lbs = {kg:.2f} kg | {g:.1f} g | {oz:.2f} oz", Colors.GREEN))
            except ValueError:
                print(color_text("Invalid input number.", Colors.RED))

        elif choice == '4':
            print("\nData Storage Conversion:")
            try:
                val = float(input("Enter value in Megabytes (MB): "))
                b = val * 1024 * 1024
                kb = val * 1024
                gb = val / 1024
                tb = gb / 1024
                print(color_text(f"\n{val} MB =", Colors.GREEN))
                print(f"  Bytes : {b:,.0f}")
                print(f"  KB    : {kb:,.2f}")
                print(f"  GB    : {gb:.4f}")
                print(f"  TB    : {tb:.6f}")
            except ValueError:
                print(color_text("Invalid input number.", Colors.RED))

        elif choice == '5':
            break

# ==========================================
# 3. CALCULATOR MODULE
# ==========================================
class Calculator:
    def __init__(self):
        self.history: List[str] = []

    def log(self, expr: str, result: Any):
        record = f"{expr} = {result}"
        self.history.append(record)
        print(color_text(f"\n[Result] {record}", Colors.GREEN))

    def show_history(self):
        if not self.history:
            print(color_text("\nNo calculation history yet.", Colors.YELLOW))
            return
        print("\n--- Calculation History ---")
        for idx, item in enumerate(self.history, 1):
            print(f"{idx}. {item}")


def run_calculator():
    calc = Calculator()
    while True:
        print("\n" + color_text("--- SCIENTIFIC CALCULATOR ---", Colors.HEADER))
        print("1. Standard Operations (+, -, *, /, %, ^)")
        print("2. Square Root & Power")
        print("3. Trigonometry (sin, cos, tan)")
        print("4. Logarithm (ln, log10)")
        print("5. View Calculation History")
        print("6. Back to Main Menu")

        choice = input(color_text("Select option (1-6): ", Colors.CYAN)).strip()

        if choice == '1':
            try:
                n1 = float(input("Enter first number: "))
                op = input("Enter operator (+, -, *, /, %, ^): ").strip()
                n2 = float(input("Enter second number: "))
                
                if op == '+': res = n1 + n2
                elif op == '-': res = n1 - n2
                elif op == '*': res = n1 * n2
                elif op == '/': 
                    if n2 == 0:
                        print(color_text("Error: Division by zero!", Colors.RED))
                        continue
                    res = n1 / n2
                elif op == '%': res = n1 % n2
                elif op == '^': res = math.pow(n1, n2)
                else:
                    print(color_text("Unknown operator.", Colors.RED))
                    continue
                
                calc.log(f"{n1} {op} {n2}", res)
            except ValueError:
                print(color_text("Invalid numeric input.", Colors.RED))

        elif choice == '2':
            try:
                val = float(input("Enter number: "))
                if val >= 0:
                    sqrt_res = math.sqrt(val)
                    calc.log(f"sqrt({val})", round(sqrt_res, 6))
                else:
                    print(color_text("Error: Cannot take square root of negative number.", Colors.RED))
            except ValueError:
                print(color_text("Invalid numeric input.", Colors.RED))

        elif choice == '3':
            try:
                deg = float(input("Enter angle in degrees: "))
                rad = math.radians(deg)
                sin_v = math.sin(rad)
                cos_v = math.cos(rad)
                tan_v = math.tan(rad) if abs(cos_v) > 1e-10 else "Undefined"
                
                print(color_text(f"\nFor {deg}°:", Colors.GREEN))
                print(f"  sin({deg}°) = {sin_v:.6f}")
                print(f"  cos({deg}°) = {cos_v:.6f}")
                print(f"  tan({deg}°) = {tan_v if isinstance(tan_v, str) else f'{tan_v:.6f}'}")
                calc.log(f"Trig({deg}°)", f"sin={sin_v:.4f}, cos={cos_v:.4f}")
            except ValueError:
                print(color_text("Invalid numeric input.", Colors.RED))

        elif choice == '4':
            try:
                val = float(input("Enter positive number: "))
                if val <= 0:
                    print(color_text("Logarithm requires positive number.", Colors.RED))
                    continue
                ln_v = math.log(val)
                log10_v = math.log10(val)
                print(color_text(f"\nFor {val}:", Colors.GREEN))
                print(f"  Natural Log (ln)  : {ln_v:.6f}")
                print(f"  Base-10 Log (log) : {log10_v:.6f}")
                calc.log(f"ln({val})", round(ln_v, 6))
            except ValueError:
                print(color_text("Invalid numeric input.", Colors.RED))

        elif choice == '5':
            calc.show_history()

        elif choice == '6':
            break

# ==========================================
# MAIN APPLICATION ROUTER
# ==========================================
def display_banner():
    banner = """
    ==================================================
        PYTHON INTERACTIVE UTILITY SUITE v1.0
    ==================================================
    """
    print(color_text(banner, Colors.CYAN))

def main():
    display_banner()
    while True:
        print("\n" + color_text("--- MAIN MENU ---", Colors.BOLD))
        print("1. Task Manager (Manage TODOs & Priorities)")
        print("2. Unit Converter (Temperature, Weight, Distance, Storage)")
        print("3. Scientific Calculator")
        print("4. Exit Application")

        choice = input(color_text("\nEnter choice (1-4): ", Colors.YELLOW)).strip()

        if choice == '1':
            run_task_manager()
        elif choice == '2':
            run_unit_converter()
        elif choice == '3':
            run_calculator()
        elif choice == '4':
            print(color_text("\nThank you for using Python Utility Suite! Goodbye.\n", Colors.GREEN))
            sys.exit(0)
        else:
            print(color_text("Invalid choice, please select 1-4.", Colors.RED))

if __name__ == "__main__":
    main()

