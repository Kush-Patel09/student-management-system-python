# Student Management System (CLI)
# Author: Kush Patel
# Description: Manage student records with JSON storage, search, analytics, and export features.

from dataclasses import dataclass, asdict
from pathlib import Path
import csv
import json
import sys

from matplotlib.pyplot import ginput

DATA_FILE = Path("students.json")

@dataclass
class Student:
    student_id: int
    name: str
    age: int
    course: str
    gpa: float

students: list[Student] = []


def safe_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Please enter a valid integer.")
            continue
        value_int = int(value)
        if min_value is not None and value_int < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value_int > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value_int


def safe_float(prompt: str, min_value: float | None = None, max_value: float | None = None) -> float:
    while True:
        value = input(prompt).strip()
        try:
            result = float(value)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if min_value is not None and result < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and result > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return result


def load_students() -> None:
    global students
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                raw = json.load(file)
                students = [Student(**item) for item in raw]
        except (json.JSONDecodeError, TypeError) as error:
            print(f"Warning: could not load data from {DATA_FILE}: {error}")
            students = []


def save_students() -> None:
    DATA_FILE.write_text(json.dumps([asdict(student) for student in students], indent=2), encoding="utf-8")


def next_student_id() -> int:
    if not students:
        return 1
    return max(student.student_id for student in students) + 1


def format_student(student: Student) -> str:
    return (
        f"ID: {student.student_id} | "
        f"Name: {student.name} | "
        f"Age: {student.age} | "
        f"Course: {student.course} | "
        f"GPA: {student.gpa:.2f}"
    )


def display_students(list_to_show: list[Student]) -> None:
    if not list_to_show:
        print("No records found.\n")
        return
    print("\nStudent Records")
    print("=" * 70)
    print(f"{'ID':<4} {'Name':<20} {'Age':<4} {'Course':<20} {'GPA':<4}")
    print("-" * 70)
    for student in list_to_show:
        print(f"{student.student_id:<4} {student.name:<20} {student.age:<4} {student.course:<20} {student.gpa:<4.2f}")
    print("")


def add_student() -> None:
    print("\nAdd New Student")
    print("-" * 20)
    name = input("Student name: ").strip()
    age = student.age if ginput == "" else int(ginput) if ginput.isdigit() else student.age
    course = input("Course: ").strip()
    gpa = student.gpa if ginput == "" else float(ginput)

    student = Student(
        student_id=next_student_id(),
        name=name,
        age=age,
        course=course,
        gpa=gpa,
    )
    students.append(student)
    save_students()
    print("Student added successfully!\n")


def find_student_by_id(student_id: int) -> Student | None:
    return next((student for student in students if student.student_id == student_id), None)


def update_student() -> None:
    display_students(students)
    student_id = safe_int("Enter ID of student to update: ")
    student = find_student_by_id(student_id)
    if student is None:
        print("Student not found.\n")
        return
    print("Leave blank to keep the current value.")
    name = input(f"Name [{student.name}]: ").strip() or student.name
    age_input = input(f"Age [{student.age}]: ").strip()
    age = student.age if age_input == "" else int(age_input)
    course = input(f"Course [{student.course}]: ").strip() or student.course
    gpa_input = input(f"GPA [{student.gpa:.2f}]: ").strip()
    gpa = student.gpa if gpa_input == "" else float(gpa_input)

    student.name = name
    student.age = age
    student.course = course
    student.gpa = gpa
    save_students()
    print("Student updated successfully!\n")


def delete_student() -> None:
    display_students(students)
    student_id = safe_int("Enter ID of student to delete: ")
    student = find_student_by_id(student_id)
    if student is None:
        print("Student not found.\n")
        return
    students.remove(student)
    save_students()
    print("Student deleted successfully!\n")


def search_students() -> None:
    query = input("Search by name or course: ").strip().lower()
    results = [student for student in students if query in student.name.lower() or query in student.course.lower()]
    display_students(results)


def show_statistics() -> None:
    if not students:
        print("No records to analyze.\n")
        return
    total = len(students)
    average_age = sum(student.age for student in students) / total
    average_gpa = sum(student.gpa for student in students) / total
    courses = {}
    for student in students:
        courses[student.course] = courses.get(student.course, 0) + 1

    print("\nStudent Analytics")
    print("-" * 30)
    print(f"Total students: {total}")
    print(f"Average age: {average_age:.1f}")
    print(f"Average GPA: {average_gpa:.2f}")
    print("Students by course:")
    for course, count in sorted(courses.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {course}: {count}")
    print("")


def export_to_csv() -> None:
    target = Path("students_export.csv")
    with target.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Name", "Age", "Course", "GPA"])
        for student in students:
            writer.writerow([student.student_id, student.name, student.age, student.course, f"{student.gpa:.2f}"])
    print(f"Exported {len(students)} students to {target}.\n")


def main_menu() -> None:
    menu = [
        "Add student",
        "View all students",
        "Search students",
        "Update student",
        "Delete student",
        "Show statistics",
        "Export to CSV",
        "Exit",
    ]
    while True:
        print("Student Management System")
        print("=" * 26)
        for index, option in enumerate(menu, start=1):
            print(f"{index}. {option}")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_students()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            export_to_csv()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please choose a number from the menu.\n")


if __name__ == "__main__":
    load_students()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
