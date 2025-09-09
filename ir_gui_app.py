# SANS Incident Response Learning Tool - GUI Edition (Final Version)
# Author: ThiSecur and Manus
# Version: 6.0
# Requirement: PyQt6

import sys
import random
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QGroupBox,
                             QRadioButton, QMessageBox, QButtonGroup, QScrollArea,
                             QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# --- Data Structure (Unchanged) ---
incident_response_data = {
    "Preparation": {
        "description": "This phase involves making the system ready for a potential incident by implementing and testing defenses. It's about being proactive.",
        "activities": [
            "Developing and documenting an incident response plan.",
            "Establishing a formal incident response team with defined roles.",
            "Acquiring and deploying security tools (e.g., EDR, SIEM, SOAR).",
            "Conducting regular security awareness training for all employees.",
            "Performing periodic risk assessments to identify vulnerabilities.",
        ]
    },
    "Identification": {
        "description": "This phase involves detecting a deviation from normal operations and determining if it is a security incident.",
        "activities": [
            "Analyzing unusual log entries from a firewall or web server.",
            "Receiving an alert from an Intrusion Detection System (IDS).",
            "Noticing a sudden and unexplained increase in network traffic to a foreign country.",
            "A user reporting a suspicious email containing a weird attachment.",
            "Observing system files being modified or encrypted unexpectedly.",
        ]
    },
    "Containment": {
        "description": "The goal of this phase is to limit the scope and magnitude of the incident and to prevent further damage.",
        "activities": [
            "Isolating an infected laptop from the corporate network.",
            "Blocking a malicious IP address at the perimeter firewall.",
            "Temporarily disabling a compromised user account.",
            "Implementing network segmentation to stop an attack's lateral movement.",
            "Taking a compromised web server offline for forensic analysis.",
        ]
    },
    "Eradication": {
        "description": "This phase focuses on completely removing the threat from the environment to ensure the attacker cannot regain access.",
        "activities": [
            "Deleting malware and associated files from all affected systems.",
            "Patching the vulnerabilities that were exploited during the attack.",
            "Resetting all compromised user and service account passwords.",
            "Rebuilding a compromised system from a known good, trusted backup.",
            "Searching for and removing any backdoors or persistence mechanisms left by the attacker.",
        ]
    },
    "Recovery": {
        "description": "This phase involves carefully restoring systems to normal operation and monitoring to ensure the incident is truly resolved.",
        "activities": [
            "Restoring data from clean, verified backups.",
            "Bringing cleaned and patched systems back online in a phased manner.",
            "Validating that the restored systems are functioning as expected.",
            "Intensively monitoring network and system logs for any signs of reinfection or unusual activity.",
            "Communicating to stakeholders that the system is back to normal operation.",
        ]
    },
    "Lessons Learned": {
        "description": "This final phase involves analyzing the incident and the response to identify areas for improvement. This is a critical step for maturing the security posture.",
        "activities": [
            "Conducting a post-incident review meeting with all involved parties.",
            "Documenting a detailed incident timeline, from initial detection to full resolution.",
            "Analyzing the root cause of the incident to prevent recurrence.",
            "Updating the incident response plan and procedures based on what was learned.",
            "Identifying gaps in security controls and recommending new tools or policies.",
        ]
    }
}


class IRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SANS Incident Response Learning Tool v6.0")
        self.setGeometry(100, 100, 800, 700)

        self.phases = list(incident_response_data.keys())
        self.quiz_questions = []
        self.user_answers = {}
        self.current_question_index = 0
        self.is_quiz_active = False

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.create_main_menu_screen()
        self.create_learn_screen()
        self.create_quiz_screen()
        self.create_results_screen()

    def create_main_menu_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("Incident Response Learning Tool")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        learn_button = QPushButton("Learn About the IR Phases")
        learn_button.setFixedSize(300, 50)
        learn_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.learn_screen))
        test_button = QPushButton("Test Your Knowledge")
        test_button.setFixedSize(300, 50)
        test_button.clicked.connect(self.start_quiz)
        exit_button = QPushButton("Exit")
        exit_button.setFixedSize(300, 50)
        exit_button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(learn_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(test_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_menu_screen = screen
        self.stacked_widget.addWidget(self.main_menu_screen)

    def create_learn_screen(self):
        self.learn_screen = QWidget()
        main_layout = QVBoxLayout(self.learn_screen)
        title = QLabel("Learn About the Phases")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.learn_content_label = QLabel("Select a phase from the buttons below.")
        self.learn_content_label.setWordWrap(True)
        self.learn_content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_box = QGroupBox("Details")
        content_layout = QVBoxLayout(content_box)
        content_layout.addWidget(self.learn_content_label)
        buttons_layout = QHBoxLayout()
        for phase in self.phases:
            btn = QPushButton(phase)
            btn.clicked.connect(lambda checked, p=phase: self.show_phase_details(p))
            buttons_layout.addWidget(btn)
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        main_layout.addWidget(title)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(content_box, 1)
        main_layout.addWidget(home_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.stacked_widget.addWidget(self.learn_screen)

    def show_phase_details(self, phase_name):
        info = incident_response_data[phase_name]
        description = info['description']
        activities_html = "".join(["<li>{}</li>".format(act) for act in info['activities']])
        details_text = "<b>Description:</b><p>{}</p><b>Example Activities:</b><ul>{}</ul>".format(description, activities_html)
        self.learn_content_label.setText(details_text)

    def create_quiz_screen(self):
        self.quiz_screen = QWidget()
        layout = QVBoxLayout(self.quiz_screen)
        self.progress_label = QLabel()
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Arial", 14))
        self.options_group = QGroupBox("Which phase does this activity belong to?")
        options_layout = QVBoxLayout()
        self.button_group = QButtonGroup()
        self.radio_buttons_map = {}
        for phase in self.phases:
            rb = QRadioButton(phase)
            self.button_group.addButton(rb)
            self.radio_buttons_map[phase] = rb
            options_layout.addWidget(rb)
        self.options_group.setLayout(options_layout)
        self.button_group.buttonClicked.connect(self.save_answer)
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("<< Previous")
        self.prev_button.clicked.connect(self.prev_question)
        self.next_button = QPushButton("Next >>")
        self.next_button.clicked.connect(self.next_question)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)
        control_layout = QHBoxLayout()
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.confirm_exit_quiz)
        evaluate_button = QPushButton("Evaluate Quiz")
        evaluate_button.clicked.connect(self.confirm_evaluate_quiz)
        exit_button = QPushButton("Exit Application")
        exit_button.clicked.connect(QApplication.instance().quit)
        control_layout.addWidget(home_button)
        control_layout.addStretch()
        control_layout.addWidget(evaluate_button)
        control_layout.addStretch()
        control_layout.addWidget(exit_button)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.question_label)
        layout.addWidget(self.options_group)
        layout.addStretch()
        layout.addLayout(nav_layout)
        layout.addLayout(control_layout)
        self.stacked_widget.addWidget(self.quiz_screen)

    def create_results_screen(self):
        self.results_screen = QWidget()
        layout = QVBoxLayout(self.results_screen)
        title = QLabel("Quiz Evaluation")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.score_label = QLabel()
        self.score_label.setFont(QFont("Arial", 16))
        self.recommendations_label = QLabel()
        self.recommendations_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        review_box = QGroupBox("Detailed Review")
        review_layout = QVBoxLayout(review_box)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.review_content_widget = QWidget()
        self.review_list_layout = QVBoxLayout(self.review_content_widget)
        self.review_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(self.review_content_widget)
        review_layout.addWidget(scroll_area)
        
        # --- CHANGE HERE: Added the "Save Quiz" button ---
        bottom_layout = QHBoxLayout()
        new_test_button = QPushButton("New Test")
        new_test_button.clicked.connect(self.confirm_new_test)
        save_button = QPushButton("Save Quiz") # New button
        save_button.clicked.connect(self.save_results_to_file) # Connects directly to the save function
        home_button = QPushButton("Return to Home")
        home_button.clicked.connect(self.confirm_exit_results)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(new_test_button)
        bottom_layout.addWidget(save_button) # Add to layout
        bottom_layout.addWidget(home_button)
        
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.recommendations_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(review_box)
        layout.addLayout(bottom_layout)
        self.stacked_widget.addWidget(self.results_screen)

    def start_quiz(self):
        self.quiz_questions = []
        for phase, data in incident_response_data.items():
            for activity in data['activities']:
                self.quiz_questions.append({"activity": activity, "correct_phase": phase})
        random.shuffle(self.quiz_questions)
        self.user_answers = {}
        self.current_question_index = 0
        self.is_quiz_active = True
        self.show_question()
        self.stacked_widget.setCurrentWidget(self.quiz_screen)

    def show_question(self):
        question_data = self.quiz_questions[self.current_question_index]
        self.progress_label.setText("Question {} of {}".format(self.current_question_index + 1, len(self.quiz_questions)))
        self.question_label.setText("<b>Activity:</b><br>'{}'".format(question_data['activity']))
        self.button_group.blockSignals(True)
        saved_answer = self.user_answers.get(self.current_question_index)
        if saved_answer:
            button_to_check = self.radio_buttons_map.get(saved_answer)
            if button_to_check:
                button_to_check.setChecked(True)
        else:
            checked_button = self.button_group.checkedButton()
            if checked_button:
                self.button_group.setExclusive(False)
                checked_button.setChecked(False)
                self.button_group.setExclusive(True)
        self.button_group.blockSignals(False)
        self.prev_button.setEnabled(self.current_question_index > 0)
        self.next_button.setEnabled(self.current_question_index < len(self.quiz_questions) - 1)

    def save_answer(self, button):
        self.user_answers[self.current_question_index] = button.text()

    def next_question(self):
        if self.current_question_index < len(self.quiz_questions) - 1:
            self.current_question_index += 1
            self.show_question()

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def confirm_evaluate_quiz(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Evaluate Quiz?")
        dialog.setText("Are you sure you want to finish and evaluate the quiz?")
        yes_button = dialog.addButton("Yes, Evaluate", QMessageBox.ButtonRole.YesRole)
        no_button = dialog.addButton("No, Continue Answering", QMessageBox.ButtonRole.NoRole)
        dialog.exec()
        if dialog.clickedButton() == yes_button:
            self.evaluate_quiz()

    def evaluate_quiz(self):
        self.is_quiz_active = False
        while self.review_list_layout.count():
            child = self.review_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        score = 0
        wrong_answers_by_phase = {phase: 0 for phase in self.phases}
        for i, question in enumerate(self.quiz_questions):
            user_answer = self.user_answers.get(i, "Not Answered")
            correct_answer = question["correct_phase"]
            is_correct = (user_answer == correct_answer)
            if is_correct:
                score += 1
                status_text = "<font color='green'>Correct</font>"
            else:
                wrong_answers_by_phase[correct_answer] += 1
                status_text = "<font color='red'>Incorrect</font>"
            review_item = QLabel(
                "<b>Q{}:</b> {}<br>"
                "Your Answer: {}<br>"
                "Correct Answer: {}<br>"
                "Status: {}".format(i + 1, question['activity'], user_answer, correct_answer, status_text)
            )
            review_item.setWordWrap(True)
            self.review_list_layout.addWidget(review_item)
            separator = QGroupBox()
            separator.setFixedHeight(2)
            self.review_list_layout.addWidget(separator)
        total = len(self.quiz_questions)
        percentage = (score / total) * 100 if total > 0 else 0
        self.score_label.setText("Your Score: {} out of {} ({:.2f}%)".format(score, total, percentage))
        max_wrong = 0
        phases_to_study = []
        for phase in self.phases:
            count = wrong_answers_by_phase[phase]
            if count > 0 and count > max_wrong:
                max_wrong = count
                phases_to_study = [phase]
            elif count > 0 and count == max_wrong:
                phases_to_study.append(phase)
        if not phases_to_study:
            self.recommendations_label.setText("<font color='green'>Excellent work! All answers were correct.</font>")
        else:
            self.recommendations_label.setText("<font color='orange'>Study Recommendation(s): {}</font>".format(", ".join(phases_to_study)))
        self.stacked_widget.setCurrentWidget(self.results_screen)

    def confirm_new_test(self):
        self.show_confirmation_dialog("Are you sure you want to start a new test?", self.start_quiz, offer_save=True)

    def confirm_exit_quiz(self):
        self.show_confirmation_dialog("Are you sure you want to exit the quiz?", self.go_home, offer_save=True)

    def confirm_exit_results(self):
        self.show_confirmation_dialog("Are you sure you want to return to the main menu?", self.go_home, offer_save=False)

    def show_confirmation_dialog(self, message, yes_action, offer_save):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Confirm Action")
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if offer_save:
            dialog.setInformativeText("Your current results will be lost unless saved.")
            save_button = dialog.addButton("Save Results", QMessageBox.ButtonRole.ActionRole)
        dialog.exec()
        clicked_button = dialog.clickedButton()
        if offer_save and clicked_button == save_button:
            self.save_results_to_file(and_then_do=yes_action)
        elif dialog.standardButton(clicked_button) == QMessageBox.StandardButton.Yes:
            yes_action()

    def save_results_to_file(self, and_then_do=None):
        if self.stacked_widget.currentWidget() == self.quiz_screen:
            self.evaluate_quiz()
        report_text = []
        report_text.append("Incident Response Quiz Results")
        report_text.append("Generated on: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        report_text.append("-" * 30)
        report_text.append(self.score_label.text())
        report_text.append(self.recommendations_label.text().replace("<font color='orange'>", "").replace("</font>", "").replace("<font color='green'>", ""))
        report_text.append("\n--- Detailed Review ---\n")
        for i in range(self.review_list_layout.count()):
            widget = self.review_list_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                clean_text = widget.text().replace("<br>", "\n").replace("<b>", "").replace("</b>", "").replace("<font color='green'>", "").replace("<font color='red'>", "").replace("</font>", "")
                report_text.append(clean_text)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Results", "ir_quiz_results.txt", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("\n".join(report_text))
                if and_then_do:
                    and_then_do()
            except Exception as e:
                QMessageBox.critical(self, "Error", "Could not save file: {}".format(e))

    def go_home(self):
        self.is_quiz_active = False
        self.stacked_widget.setCurrentWidget(self.main_menu_screen)

def main():
    app = QApplication(sys.argv)
    window = IRApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
