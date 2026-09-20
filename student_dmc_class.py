# ==============================================================================
#           STUDENT DETAILED MARKS CERTIFICATE (DMC) GENERATOR (OOP CLASS VERSION)
# ==============================================================================
# Description:
#   An Object-Oriented Python application using Classes (Subject, Student, 
#   DMCReport, InputValidator, DMCApplication) to collect student details,
#   validate marks, compute grades/status, print formatted DMC certificates,
#   and save them to text files.
#
# How to Run:
#   1. Open terminal/command prompt.
#   2. Run: python student_dmc_class.py
# ==============================================================================

import os


class Subject:
    """Represents an individual academic subject with marks and evaluation logic."""

    def __init__(self, name: str, max_marks: float, obtained_marks: float):
        self.name = name
        self.max_marks = max_marks
        self.obtained_marks = obtained_marks

    @property
    def percentage(self) -> float:
        """Calculates percentage for this subject."""
        if self.max_marks <= 0:
            return 0.0
        return (self.obtained_marks / self.max_marks) * 100.0

    @property
    def is_passed(self) -> bool:
        """Subject passing requirement: minimum 40%."""
        return self.percentage >= 40.0

    @property
    def status_label(self) -> str:
        """Returns PASS or FAIL* string representation."""
        return "PASS" if self.is_passed else "FAIL*"


class Student:
    """Represents a student, managing their profile and collection of subjects."""

    def __init__(self, name: str, roll_number: str, class_name: str, school_name: str):
        self.name = name
        self.roll_number = roll_number
        self.class_name = class_name
        self.school_name = school_name
        self.subjects: list[Subject] = []

    def add_subject(self, subject: Subject):
        """Adds a Subject object to the student's record."""
        self.subjects.append(subject)

    @property
    def total_max_marks(self) -> float:
        """Calculates sum of max marks across all subjects."""
        return sum(s.max_marks for s in self.subjects)

    @property
    def total_obtained_marks(self) -> float:
        """Calculates sum of obtained marks across all subjects."""
        return sum(s.obtained_marks for s in self.subjects)

    @property
    def overall_percentage(self) -> float:
        """Calculates total percentage for the student."""
        total_max = self.total_max_marks
        if total_max <= 0:
            return 0.0
        return (self.total_obtained_marks / total_max) * 100.0

    @property
    def failed_any_subject(self) -> bool:
        """Returns True if the student scored below 40% in any subject."""
        return any(not s.is_passed for s in self.subjects)

    @property
    def result_status(self) -> str:
        """
        Determines PASS/FAIL status:
        Fails if overall percentage < 50% OR failed any individual subject.
        """
        if self.failed_any_subject or self.overall_percentage < 50.0:
            return "FAIL"
        return "PASS"

    @property
    def grade(self) -> str:
        """
        Calculates letter grade:
        - A+ : >= 90%
        - A  : 80% to 89.99%
        - B  : 70% to 79.99%
        - C  : 60% to 69.99%
        - D  : 50% to 59.99%
        - F  : Below 50% or failed any subject
        """
        if self.result_status == "FAIL":
            return "F"

        pct = self.overall_percentage
        if pct >= 90.0:
            return "A+"
        elif pct >= 80.0:
            return "A"
        elif pct >= 75.0:
            return "B"
        elif pct >= 60.0:
            return "C"
        else:
            return "D"


class DMCReport:
    """Handles formatting and exporting Detailed Marks Certificates (DMC)."""

    @staticmethod
    def generate_text(student: Student) -> str:
        """Formats student evaluation data into an ASCII table DMC layout."""
        width = 74
        lines = []

        lines.append("=" * width)
        lines.append("                DETAILED MARKS CERTIFICATE (DMC)                ".center(width))
        lines.append(f"{student.school_name.upper()}".center(width))
        lines.append("=" * width)
        lines.append(f" Student Name : {student.name}")
        lines.append(f" Roll Number  : {student.roll_number}")
        lines.append(f" Class/Sem    : {student.class_name}")
        lines.append("-" * width)

        sub_title = "Subject Name"
        max_title = "Max Marks"
        obt_title = "Obtained"
        pct_title = "% Age"
        st_title  = "Status"
        lines.append(f"| {sub_title:<24} | {max_title:>10} | {obt_title:>10} | {pct_title:>8} | {st_title:<6} |")
        lines.append("-" * width)

        for s in student.subjects:
            lines.append(
                f"| {s.name:<24} | {s.max_marks:>10.1f} | {s.obtained_marks:>10.1f} | {s.percentage:>7.2f}% | {s.status_label:<6} |"
            )

        lines.append("-" * width)
        lines.append(f" Total Maximum Marks  : {student.total_max_marks:.1f}")
        lines.append(f" Total Obtained Marks : {student.total_obtained_marks:.1f}")
        lines.append(f" Overall Percentage   : {student.overall_percentage:.2f}%")
        lines.append(f" Final Grade          : {student.grade}")
        lines.append(f" Result Status        : {student.result_status}")
        if student.failed_any_subject:
            lines.append(" (*Note: Scored below 40% passing mark in one or more subjects)")
        lines.append("=" * width)

        return "\n".join(lines)

    @staticmethod
    def save_to_file(student: Student, dmc_content: str) -> str | None:
        """Saves formatted DMC report to a text file named dmc_<roll_number>.txt."""
        safe_roll = "".join(c for c in student.roll_number if c.isalnum() or c in ("-", "_")).strip()
        if not safe_roll:
            safe_roll = "student"

        filename = f"dmc_{safe_roll}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(dmc_content + "\n")
            print(f"\n [Success] DMC certificate successfully saved to file: '{filename}'")
            return filename
        except Exception as e:
            print(f"\n [Error] Could not save DMC file: {e}")
            return None


class InputValidator:
    """Utility class for validating user CLI inputs."""

    @staticmethod
    def get_non_empty_string(prompt: str) -> str:
        """Prompts for non-empty text input."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("  [Error] Input cannot be empty. Please try again.")

    @staticmethod
    def get_positive_float(prompt: str, allow_zero: bool = False) -> float:
        """Prompts for a valid positive (or non-negative) number."""
        while True:
            raw_input = input(prompt).strip()
            try:
                val = float(raw_input)
                if allow_zero and val < 0:
                    print("  [Error] Marks cannot be negative. Please enter a value >= 0.")
                elif not allow_zero and val <= 0:
                    print("  [Error] Value must be greater than zero. Please try again.")
                else:
                    return val
            except ValueError:
                print("  [Error] Invalid input. Please enter a valid number (e.g. 100 or 85.5).")

    @staticmethod
    def get_valid_obtained_marks(prompt: str, max_marks: float) -> float:
        """Ensures obtained marks are non-negative and do not exceed maximum marks."""
        while True:
            obtained = InputValidator.get_positive_float(prompt, allow_zero=True)
            if obtained > max_marks:
                print(f"  [Error] Obtained marks ({obtained}) cannot exceed maximum marks ({max_marks}).")
            else:
                return obtained

    @staticmethod
    def get_positive_int(prompt: str) -> int:
        """Prompts for a positive integer input."""
        while True:
            raw_input = input(prompt).strip()
            try:
                val = int(raw_input)
                if val <= 0:
                    print("  [Error] Value must be an integer greater than zero.")
                    continue
                return val
            except ValueError:
                print("  [Error] Please enter a valid integer.")


class DMCApplication:
    """Main CLI Application controller class managing menus and flow."""

    def print_header(self, title: str):
        """Prints styled section header."""
        width = 68
        print("\n" + "=" * width)
        print(f" {title.upper()} ".center(width, "="))
        print("=" * width)

    def collect_student_data(self) -> Student:
        """Prompts user for student details and subject marks, returning a Student object."""
        self.print_header("Enter Student Details")
        
        name = InputValidator.get_non_empty_string("Enter Student Full Name    : ")
        roll_number = InputValidator.get_non_empty_string("Enter Roll Number / ID     : ")
        class_name = InputValidator.get_non_empty_string("Enter Class / Semester     : ")
        school_name = InputValidator.get_non_empty_string("Enter School / College Name: ")

        student = Student(name, roll_number, class_name, school_name)

        self.print_header("Enter Subject Marks Details")
        num_subjects = InputValidator.get_positive_int("Enter total number of subjects: ")

        print("\nEnter subject details below:")
        for i in range(1, num_subjects + 1):
            print(f"\n--- Subject #{i} ---")
            sub_name = InputValidator.get_non_empty_string(f"Subject #{i} Name             : ")
            max_m = InputValidator.get_positive_float(f"Maximum Marks for '{sub_name}': ", allow_zero=False)
            obt_m = InputValidator.get_valid_obtained_marks(f"Obtained Marks for '{sub_name}': ", max_m)

            subject = Subject(sub_name, max_m, obt_m)
            student.add_subject(subject)

        return student

    def show_grading_rules(self):
        """Displays grading scale and pass/fail rules."""
        self.print_header("DMC Grading Scale & Rules")
        print("""
  GRADING SCALE:
    - Grade A+ : 90% and above
    - Grade A  : 80% to 89.99%
    - Grade B  : 70% to 79.99%
    - Grade C  : 60% to 69.99%
    - Grade D  : 50% to 59.99%
    - Grade F  : Below 50% OR scored < 40% in any subject

  PASSING RULES:
    1. A student MUST score at least 40% in EACH individual subject.
    2. Scoring below 40% in ANY subject leads to an overall FAIL status.
    3. An overall percentage of at least 50% is required to PASS.
        """)

    def run(self):
        """Main application execution loop."""
        while True:
            self.print_header("STUDENT DMC APPLICATION MENU (OOP)")
            print("  1. Create New Student DMC")
            print("  2. View Grading Scale & Rules")
            print("  3. Exit Program")
            print("-" * 68)

            choice = input("Select an option (1-3): ").strip()

            if choice == "1":
                student = self.collect_student_data()
                dmc_text = DMCReport.generate_text(student)

                print("\n")
                print(dmc_text)

                DMCReport.save_to_file(student, dmc_text)

                input("\nPress ENTER to return to the main menu...")

            elif choice == "2":
                self.show_grading_rules()
                input("\nPress ENTER to return to the main menu...")

            elif choice == "3":
                print("\nThank you for using the Object-Oriented Student DMC Generator. Goodbye!\n")
                break

            else:
                print("  [Error] Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    app = DMCApplication()
    app.run()
