# This is the Interview Helper app I started codding it at 7/Oct/2024
import os
import sys
import pygame
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QSizePolicy, QTextEdit,
                             QMessageBox, QGroupBox, QFormLayout, QDialog, QMenuBar,
                             QAction)
from PyQt5.QtGui import QPixmap, QIcon, QTransform
from PyQt5.QtCore import Qt, QTimer


WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
PICTURE_WIDTH = 150
PICTURE_HEIGHT = 150
GROUP_BOXES_WIDTH = 700
GROUP_BOXES_HEIGHT = 400
user_names = ("abdiladif ali ibrahim", "abdirahman mahamed ibrahim")


# I used this function because the pyinstaller expects to find all the
# resource file inside temporary file called sys._MEIPASS
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class EditDataDialog(QDialog):
    def __init__(self, current_data, filename, parent=None):
        super().__init__(parent)
        self.current_data = current_data
        self.filename = filename
        self.initUI()

    def initUI(self):
        # Set dialog window size
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout()

        # Add label
        label = QLabel(f"Editing {self.filename}")
        layout.addWidget(label)

        # Add text edit with current data
        self.text_edit = QTextEdit()
        self.text_edit.setText('\n'.join(self.current_data))
        layout.addWidget(self.text_edit)

        # Add buttons in bottom right corner
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push buttons to the right

        save_button = QPushButton('Save')
        cancel_button = QPushButton('Cancel')

        # Style the buttons
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745; 
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle(f'Edit {self.filename}')

    def get_updated_data(self):
        return self.text_edit.toPlainText().split('\n')

class InterviewApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interview Helper!")
        self.setWindowIcon(QIcon(resource_path(".\\Images\\icon.png")))
        self.user_name = QLabel("Magaca:", self)
        self.user_input = QLineEdit(self)
        self.submit_button = QPushButton("Submit && Clear", self)
        self.introduction_text = QTextEdit(self)
        self.introduction_text.setReadOnly(True)
        self.abdiladif_pixmap = QPixmap(resource_path("Images\\abdiladif ali ibrahim.jpg"))
        self.abdirahman_pixmap = QPixmap(resource_path("Images\\abdirahman mahamed ibrahim.jpg"))
        self.user_pic_label = QLabel(self)
# TODO: FIX ABDIRAHMAN'S IMAGE ROTATION
        # Usage example:
        # pixmap = QPixmap("Images\\abdirahman mahamed ibrahim.jpg")
        self.rotated_pixmap = self.rotate_image(self.abdirahman_pixmap, 0)  # Rotate 90 degrees clockwise
        # self.user_pic_label.setPixmap(rotated_pixmap)

        self.interv_pixmap = QPixmap(resource_path("./Images/interviewerpix.jpg"))
        self.interv_label = QLabel("interviewer:", self)
        self.interv_name = QLabel("Magaca interviewer-ka", self)
        self.intervr_pic_label = QLabel(self)
        self.ques_label = QLabel(self)
        self.ques_text = QTextEdit(self)
        self.ques_text.setReadOnly(True)
        self.answer_label = QLabel("Answer 1:", self)
        self.answer_text = QTextEdit(self)
        self.answer_text.setReadOnly(True)
        self.right_answer_button = QPushButton("Jawaab Sax ah", self)
        self.wrong_answer_button = QPushButton("Jawaab Qaldan", self)
        self.ques_timer = QTimer(self)
        self.ques_timer_label = QLabel("Question Timer", self)
        self.timer_button = QPushButton("Start", self)

        pygame.mixer.init()
        self.sound_file = resource_path("Sound\\ticking-clock.mp3")
        self.tick_sound = pygame.mixer.Sound(self.sound_file)
        self.tick_channel = pygame.mixer.Channel(0)
        self.answers = []
        self.questions = []
        self.set_ques_ans()
        self.ques_answ = []
        self.ques_num = 0
        self.ans_num = 0
        self.score = 0
        self.total_questions = 0  # Add this to track total questions attempted

        self.question_time = 11
        self.set_timer = False
        self.current_quest_index = -1  # I used -1 so that the first element of the list is included.
        self.current_ans_index = -1
        self.initUI()

    def initUI(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.user_pic_label.setFixedSize(PICTURE_WIDTH, PICTURE_HEIGHT)
        self.user_pic_label.setScaledContents(True)
        self.intervr_pic_label.setPixmap(self.interv_pixmap)
        self.intervr_pic_label.setFixedSize(PICTURE_WIDTH, PICTURE_HEIGHT)
        self.intervr_pic_label.setScaledContents(True)
        self.submit_button.setFixedSize(200, 40)
        self.answer_text.setFixedSize(750, 550)
        self.ques_text.setFixedSize(750, 150)
        self.timer_button.setFixedSize(200, 40)
        self.ques_timer_label.setWordWrap(True)
        self.user_input.setPlaceholderText("Halkan magaca qofka.")
        self.ques_label.setText(f"Quesion {self.ques_num}:")
        self.answer_label.setText(f"Answer {self.ans_num}:")
        self.ques_text.setPlainText("Waiting for questions...")
        self.answer_text.setPlainText("Waiting for answers...")
        self.ques_text.setAcceptRichText(True)
        self.answer_text.setAcceptRichText(True)

        group_box = QGroupBox("Personal Information")
        group_box1 = QGroupBox("Timer")

        # This controls the size and expanding of the two groups Timer and above it.
        group_box.setFixedSize(GROUP_BOXES_WIDTH, GROUP_BOXES_HEIGHT)
        group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        group_box1.setFixedSize(GROUP_BOXES_WIDTH, GROUP_BOXES_HEIGHT)
        group_box1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Laba sawir isku dul dhigayaa.
        v_layout1 = QVBoxLayout()
        v_layout1.addWidget(self.user_pic_label)
        v_layout1.addWidget(self.intervr_pic_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        v_for_timer = QVBoxLayout()
        # v_for_timer.addWidget(self.timer_label) # kani waa timer kii la shaqaynayay welcome text-ga waa iska yar joojiyay.
        v_for_timer.addWidget(self.ques_timer_label)
        v_for_timer.addWidget(self.timer_button, alignment=Qt.AlignRight)
        group_box1.setLayout(v_for_timer)

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.right_answer_button)
        h_layout1.addWidget(self.wrong_answer_button)

        v_layout_for_right_side = QVBoxLayout()
        v_layout_for_right_side.addWidget(self.ques_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        v_layout_for_right_side.addWidget(self.ques_text)
        v_layout_for_right_side.addWidget(self.answer_label)
        v_layout_for_right_side.addWidget(self.answer_text)
        v_layout_for_right_side.addLayout(h_layout1)
        v_layout_for_right_side.setContentsMargins(0, 0, 0, 0) # Shaki baa igaga jira inuu wax soo kordhinayo.
        v_layout_for_right_side.setSpacing(10)
        v_layout_for_right_side.addStretch()

        f_layout = QFormLayout()
        f_layout.addRow(self.user_name, self.user_input)
        f_layout.addRow(self.submit_button)
        f_layout.setAlignment(self.submit_button, Qt.AlignCenter)
        f_layout.addRow(self.introduction_text)

        f_layout_inter_label = QFormLayout()
        f_layout_inter_label.addRow(self.interv_label, self.interv_name)

        v_layout3 = QVBoxLayout()
        v_layout3.addLayout(f_layout)
        v_layout3.addLayout(f_layout_inter_label)

        # Waa ka labadii Layout ee hore is barbardhigay si aan ugu daro groupka.
        h_for_group = QHBoxLayout()
        h_for_group.addLayout(f_layout)
        h_for_group.addLayout(v_layout3)
        h_for_group.addLayout(v_layout1)
        group_box.setLayout(h_for_group)

        v_2_groups = QVBoxLayout()
        v_2_groups.addWidget(group_box)
        v_2_groups.addWidget(group_box1)

        # Kani waa Layout-ka guud ee program-ka.
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(h_for_group)
        self.main_layout.addLayout(v_2_groups)
        self.main_layout.addLayout(v_layout_for_right_side)

        # Wrapper layout to contain everything
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        # Create menu bar
        self.menu_bar = QMenuBar()
        self.menu_bar.setFixedHeight(30)
        self.menu_bar.setFixedWidth(150)
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #dedddc;
                border: none;
            }
            QMenuBar::item:selected {
                background-color: #a6a6a6;
            }
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 5px 30px 5px 30px;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
        """)

        edit_menu = self.menu_bar.addMenu('Edit or Add Files')

        # Add file options to menu
        qa_files = ['abdiladifQA.txt', 'abdirahmanQA.txt']
        for file in qa_files:
            action = QAction(file, self)
            action.triggered.connect(lambda checked, f=file: self.edit_file_data(f))
            edit_menu.addAction(action)

        # Add menu bar to wrapper layout
        menu_container = QWidget()
        menu_layout = QHBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.addWidget(self.menu_bar)
        menu_layout.addStretch()
        wrapper_layout.addWidget(menu_container)

        # Add main layout to wrapper
        wrapper_layout.addLayout(self.main_layout)

        self.setLayout(wrapper_layout)

        self.user_name.setObjectName("user_name")
        # self.timer_label.setObjectName("timer") # Waa timer kii aan yar joojiyay.
        self.user_pic_label.setObjectName("pictures")
        self.intervr_pic_label.setObjectName("pictures")
        self.ques_timer_label.setObjectName("ques_timer_label")
        self.wrong_answer_button.setObjectName("wrong_answer_button")

        # This is the CSS style sheet for the main layout.
        self.setStyleSheet("""
                QTextEdit {
                    font-size: 22px;
                    font-family: Arial;
                    }
                QLineEdit {
                    font-size:22px;
                    }
                QGroupBox {
                       font: bold 16px;
                       border: 2px solid #4CAF50;
                       border-radius: 10px;
                       margin-top: 10px;
                    }
                QGroupBox::title {
                       subcontrol-origin: margin;
                       subcontrol-position: top center;
                       padding: 0 3px;
                    }

                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 5px 5px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 25px;
                    }
                QPushButton:hover {
                    background-color: #218838;
                    }
                QPushButton#wrong_answer_button{
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 5px;
                    min-width: 80px;
                }
                QPushButton#wrong_answer_button:hover {
                    background-color: #da190b;
                }
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    background-color: #f0f0f0;
                    border-radius: 3px;
                    padding: 5px;

                    }
                QLabel#user_name{
                    font-size:18px;
                    font-weight: bold;
                }
                QLabel#ques_timer_label {
                    font-size: 30px;
                    color: hsl(111, 100%, 50%);
                    background-color: black;
                    border: 5px solid blue;
                } 
                QLabel#pictures{
                    border: 4px solid #4CAF50;
                 }
               """)


        self.ques_timer.timeout.connect(self.update_timer_questions)
        self.timer_button.clicked.connect(self.start_question_timer)
        self.submit_button.clicked.connect(self.set_introduction_text_reset_display)
        self.right_answer_button.clicked.connect(self.display_question_answer_correct)
        self.wrong_answer_button.clicked.connect(self.display_question_answer_incorrect)

    # Method 2: If you want to rotate multiple images, create a function
    def rotate_image(self, pixmap, angle):
        transform = QTransform().rotate(angle)
        return pixmap.transformed(transform)

    def edit_file_data(self, selected_file):
        file_path = os.path.join('./Docs', selected_file)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                current_data = file.read().splitlines()

            dialog = EditDataDialog(current_data, selected_file, self)

            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_updated_data()

                # Save updated data
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(updated_data))

                QMessageBox.information(self, "Success", "File updated successfully!")

                # Reload questions if the current user's file was edited
                if selected_file.lower().startswith(self.user_input.text().lower()):
                    self.set_ques_ans()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error editing file: {str(e)}")

    def set_introduction_text_reset_display(self):
        self.current_quest_index = -1
        self.current_ans_index = -1
        self.ques_num = 0
        self.ans_num = 0
        self.score = 0
        self.total_questions = 0  # this track total questions attempted

        # Clear existing questions and answers
        self.questions.clear()
        self.answers.clear()

        self.select_person()
        if self.user_input.text():
            # Load questions and answers first
            self.set_ques_ans()

            # Display first question and answer
            if self.questions and self.answers:
                self.current_quest_index = 0
                self.current_ans_index = 0
                self.ques_num = 1
                self.ans_num = 1

                self.ques_text.setPlainText(self.questions[0])
                self.answer_text.setPlainText(self.answers[0])
                self.ques_label.setText(f"Question {self.ques_num}:")
                self.answer_label.setText(f"Answer {self.ans_num}:")
            else:
                self.ques_text.setPlainText("Please, Magac Sax ah geli.")
                self.answer_text.setPlainText("Please, Magac Sax ah geli.")

            self.reset_timer()
            self.timer_button.setStyleSheet("background-color: #ff0d41;")
            self.timer_button.setText("Pause")
            self.set_timer = True

    def select_person(self):
        interviewer_name = ("Rachel Notley", "Caroline Cochrane")
        user_input = self.user_input.text().lower().strip()  # lower the letters and removing
        # leading and trailing spaces
        if user_input == user_names[0]:
            self.introduction_text.setText(f"Welcome {user_input} I am {interviewer_name[0]}, "
                                           f"and I will conduct your interview today. I will "
                                           f"be having the last decision about your case, "
                                           f"so don't lie to me, ok?")
            self.interv_name.setText(interviewer_name[0])
            self.user_pic_label.setPixmap(self.abdiladif_pixmap)
        elif user_input == user_names[1]:
            self.introduction_text.setText(f"Welcome {user_input} I am {interviewer_name[1]}, "
                                           f"and I will conduct your interview today. I will "
                                           f"be having the last decision about your case, "
                                           f"so don't lie to me, ok?")
            self.interv_name.setText(interviewer_name[1])
            self.user_pic_label.setPixmap(self.rotated_pixmap)
        elif not user_input:  # This deals with when user input is empty
            self.introduction_text.setText("Halka sare magac geli.")
        else:
            self.introduction_text.setText("Magac qaldan ayaad galisay.")

    def set_ques_ans(self):
        try:
            user_input = self.user_input.text().lower()

            # Clear existing lists before loading new data
            self.questions.clear()
            self.answers.clear()

            filename = None
            if user_input == user_names[0]:
                filename = resource_path(".\\Docs\\abdiladifQA.txt")
            elif user_input == user_names[1]:
                filename = resource_path(".\\Docs\\abdirahmanQA.txt")

            if filename:
                with open(filename, "r", encoding="utf-8") as que_ans:
                    for line in que_ans:
                        line = line.strip()
                        if line.startswith("Q"):
                            self.questions.append(line)
                        elif line.startswith("A"):
                            self.answers.append(line)


        except FileNotFoundError:
            self.ques_text.setPlainText("Error: The file was not found.")
        except Exception as e:
            self.ques_text.setPlainText(f"An unexpected error occurred: {e}")

    def display_question_answer_correct(self):
        user_input = self.user_input.text().strip().lower()
        if not user_input:
            self.ques_text.setPlainText("Please Magaca geli si aad u heshid su'aasha.")
            self.answer_text.setPlainText("Please Magaca geli si aad u heshid jawaabta.")
            return
        elif user_input not in user_names:
            self.ques_text.setPlainText("Please, Magac Sax ah geli.")
            self.answer_text.setPlainText("Please, Magac Sax ah geli.")
            return

        try:
            # First check if we're already at the end
            if self.current_quest_index >= len(self.questions):
                self.show_congratulations()
                return

            # If not at the end, proceed with incrementing and showing next question
            self.score += 1
            self.total_questions += 1

            self.reset_timer()
            self.timer_button.setStyleSheet("background-color: #ff0d41;")
            self.timer_button.setText("Pause")
            self.set_timer = True

            # Move to next question
            self.current_quest_index += 1
            self.current_ans_index += 1
            self.tick_channel.stop()

            if self.current_quest_index < len(self.questions):
                self.ques_text.setPlainText(self.questions[self.current_quest_index])
                self.ques_num += 1
                self.ques_label.setText(f"Question {self.ques_num}:")

                self.answer_text.setPlainText(self.answers[self.current_ans_index])
                self.ans_num += 1
                self.answer_label.setText(f"Answer {self.ans_num}:")
            else:
                self.show_congratulations()

        except Exception as e:
            self.ques_text.setPlainText(f"An unexpected error occurred: {e}")

    def display_question_answer_incorrect(self):
        user_input = self.user_input.text().strip().lower()
        if not user_input:
            self.ques_text.setPlainText("Please Magaca geli si aad u heshid su'aasha.")
            self.answer_text.setPlainText("Please Magaca geli si aad u heshid jawaabta.")
            return
        elif user_input not in user_names:
            self.ques_text.setPlainText("Please, Magac Sax ah geli.")
            self.answer_text.setPlainText("Please, Magac Sax ah geli.")
            return

        try:
            # First check if we're already at the end
            if self.current_quest_index >= len(self.questions):
                self.show_congratulations()
                return

            # If not at the end, proceed with incrementing and showing next question
            self.total_questions += 1

            self.reset_timer()
            self.timer_button.setStyleSheet("background-color: #ff0d41;")
            self.timer_button.setText("Pause")
            self.set_timer = True

            # Move to next question
            self.current_quest_index += 1
            self.current_ans_index += 1
            self.tick_channel.stop()

            if self.current_quest_index < len(self.questions):
                self.ques_text.setPlainText(self.questions[self.current_quest_index])
                self.ques_num += 1
                self.ques_label.setText(f"Question {self.ques_num}:")

                self.answer_text.setPlainText(self.answers[self.current_ans_index])
                self.ans_num += 1
                self.answer_label.setText(f"Answer {self.ans_num}:")
            else:
                self.show_congratulations()

        except Exception as e:
            self.ques_text.setPlainText(f"An unexpected error occurred: {e}")

    def show_congratulations(self):
        total_questions = len(self.questions)
        # Calculate percentage based on the total number of questions
        score_percent = (self.score / total_questions * 100) if total_questions > 0 else 0

        # Construct the congratulatory message
        user_name = self.user_input.text().strip()  # Get the user's name

        # Check if the score is above 50% before showing the congratulatory message
        if score_percent > 50:
            congratulatory_message = f"""
               <div style='text-align: center;'>
                   <h2 style='color: #27ae60'>{user_name}, Congratulations🎉</h2>
                   <p><strong>You have passed the interview. Welcome to Canada!</strong></p><br>
                   <img src='Images/{user_name}.jpg' 
                   width='300' height='300' style='margin: 10px;'/>
                   <img src='canada_flag.png' width='300' 
                   height='300' style='margin: 10px;'/>
               </div>
               """
            success_score = f"""<p>Your score: 
                        <strong style='color: #27ae60'>{score_percent:.1f}%</strong></p> """

            # Display results in both text areas
            self.ques_text.setHtml(success_score)
            self.answer_text.setHtml(congratulatory_message)

            # Disable timer button since quiz is finished and set the text and stop it.
            self.ques_timer.stop()
            self.ques_timer_label.setText("The interview is finished!")
            self.timer_button.setText("Finished")
            self.timer_button.setEnabled(False)
        else:
            # If the score is 50% or less, show a different message
            user_name = self.user_input.text().strip()  # Get the user's name
            failure_message = f"""
                   <div style='text-align: center; color: #ff0303;'>
                       <h2>Sorry, {user_name}!</h2>
                       <p>You did not pass the interview. Better luck next time!</p><br>
                        <img src='Images/{user_name}.jpg' 
                         width='300' height='300' style='margin: 10px;'/>
                         <img src='canada_flag_failed.png' width='300' 
                         height='300' style='margin: 10px;'/>
                   </div>
                   """
            failed_score = f"""
            <p>Your score: <strong style='color: #ff0303'>{score_percent:.1f}%</strong></p> """

            # Display results in both text areas
            self.ques_text.setHtml(failed_score)
            self.answer_text.setHtml(failure_message)

            # Disable timer button since quiz is finished and set the text and stop it.
            self.ques_timer.stop()
            self.ques_timer_label.setText("The interview is finished!")
            self.timer_button.setText("Finished")
            self.timer_button.setEnabled(False)


    def start_question_timer(self):
        # I did this logic for the pausing of the timer/resuming.
        try:
            if not self.set_timer:
                if self.question_time == 0:
                    self.reset_timer()
                self.ques_timer.start(1000)
                self.set_timer = True
                self.timer_button.setStyleSheet("background-color: #ff0d41;")
                self.timer_button.setText("Pause")
            elif self.set_timer:
                self.ques_timer.stop()
                self.tick_sound.stop()
                self.set_timer = False
                self.timer_button.setStyleSheet("background-color: #4CAF50;")
                self.timer_button.setText("Resume")
        except Exception as b:
            print(b)

    def update_timer_questions(self):
        if self.question_time > 0:
            self.ques_timer.start(1000)  # Update every second
            self.question_time -= 1
            centered_text_question = f'''{self.user_input.text()[:9]} Wakhtiga Su'aasha aad u haysatid waa: <div style="
                                        text-align: center; font-size: 200px;">{self.question_time}
                                            </div> '''
            self.ques_timer_label.setText(centered_text_question)
            self.tick_channel.play(self.tick_sound)

        elif self.question_time == 0 or self.set_timer:
            self.ques_timer.stop()
            failed_ques_text = f"{self.user_input.text()} Waad ku Dhacday Su'aashaas 😟"
            self.ques_timer_label.setText(failed_ques_text)
            self.tick_channel.stop()
            self.timer_button.setStyleSheet("background-color: #4CAF50;")
            self.set_timer = False
            self.timer_button.setText("Start")

    def reset_timer(self):
        self.question_time = 11
        self.ques_timer.start(1000)
        self.timer_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    interview_window = InterviewApp()
    interview_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()