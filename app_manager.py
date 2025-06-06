import json
import os

PROGRAMS_FILE = "programs.json"


def load_programs():
    if not os.path.exists(PROGRAMS_FILE):
        return []
    try:
        with open(PROGRAMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Failed to read file. It may be corrupted.")
        return []


def save_programs(programs):
    with open(PROGRAMS_FILE, "w", encoding="utf-8") as f:
        json.dump(programs, f, indent=4, ensure_ascii=False)


def find_program_by_name(name, programs):
    return next((p for p in programs if p["name"] == name), None)


def add_program(name, source, args, priority):
    programs = load_programs()
    if find_program_by_name(name, programs):
        print(f"A program named '{name}' already exists.")
        return

    new_program = {
        "name": name,
        "source": source,
        "install_args": args,
        "priority": priority
    }
    programs.append(new_program)
    save_programs(programs)
    print(f"✅ Program '{name}' has been successfully added.")


def remove_program(name):
    programs = load_programs()
    program = find_program_by_name(name, programs)
    if not program:
        print(f"❌ Program '{name}' not found.")
        return

    programs.remove(program)
    save_programs(programs)
    print(f"🗑️ Program '{name}' has been removed.")


def edit_program(old_name, new_name, source, args, priority):
    programs = load_programs()
    program = find_program_by_name(old_name, programs)
    if not program:
        print(f"❌ Program '{old_name}' not found.")
        return

    program.update({
        "name": new_name,
        "source": source,
        "install_args": args,
        "priority": priority
    })
    save_programs(programs)
    print(f"✏️ Program '{old_name}' has been updated to '{new_name}'.")


def list_programs():
    programs = load_programs()
    if not programs:
        print("📂 Program list is empty.")
        return

    print("\n📋 Program list:")
    for p in sorted(programs, key=lambda x: x["priority"]):
        print(f"Name: {p['name']}\nSource: {p['source']}\nArguments: {p['install_args']}\nPriority: {p['priority']}")
        print("-" * 30 + "\n")


def get_valid_priority():
    while True:
        try:
            priority = int(input("Enter priority (an integer): "))
            return priority
        except ValueError:
            print("⚠️ Please enter an integer!")


def manage_programs():
    while True:
        print("1. Add program")
        print("2. Remove program")
        print("3. Edit program")
        print("4. Show program list")
        print("5. Run installer")
        print("6. Exit")

        choice = input("Select action (1-6): ").strip()

        if choice == "1":
            name = input("Enter program name: ")
            source = input("Enter source (URL or path): ")
            args = input("Enter install arguments: ")
            priority = get_valid_priority()
            add_program(name, source, args, priority)

        elif choice == "2":
            name = input("Enter the name of the program to remove: ")
            remove_program(name)

        elif choice == "3":
            old_name = input("Enter current program name: ")
            new_name = input("Enter new name: ")
            source = input("Enter new source: ")
            args = input("Enter new arguments: ")
            priority = get_valid_priority()
            edit_program(old_name, new_name, source, args, priority)

        elif choice == "4":
            list_programs()

        elif choice == "5":
            from installer import run_installer
            run_installer()

        elif choice == "6":
            print("👋 Exiting program.")
            break

        else:
            print("❗ Invalid choice. Please select a number from 1 to 6.")