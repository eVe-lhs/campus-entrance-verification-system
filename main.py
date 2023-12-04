import sys
import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap, QImage,QFont
import os
import mediapipe as mp
import numpy as np
import re
import cv2
from qr_code_scanner import scan_qr_code
from face_recog import FaceRecognition
from video_license_plate2 import detect_plate

mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.8)
class Home(QWidget):
    license_plate_result = ''
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        

        font = QFont("Helvetica [Cronyx]", 24 , QFont.Weight.Bold)
        self.label = QLabel("Campus Entrance Security")
        self.label.setFont(font)
        layout.addWidget(self.label)
        # self.sButton = QPushButton("Student Entry")
        # self.sButton.clicked.connect(self.run_recognition)
        # layout.addWidget(self.sButton)
        #
        # self.cButton = QPushButton("Car Entry")
        # self.cButton.clicked.connect(self.stop_run_recognition)
        # layout.addWidget(self.cButton)

        self.fButton = QPushButton("New Student Register",self)
        self.fButton.clicked.connect(self.go_to_form)
        layout.addWidget(self.fButton)

        self.cButton = QPushButton("Car Entry",self)
        self.cButton.clicked.connect(self.scan_license)
        layout.addWidget(self.cButton)

        self.sButton = QPushButton("Student Entry",self)
        self.sButton.clicked.connect(self.go_student_entry)
        layout.addWidget(self.sButton)

        self.setStyleSheet(
            """
            background-color: #f0f0f0;
            """
        )

        self.label.setStyleSheet("""
            background-color: #3498db;
            color: #ffffff;
            border: 2px solid #34495e;
            border-radius: 10px;
            padding: 10px;
            """
)   
        style = """
                QPushButton {
                    background-color: #4CAF50; /* Green background color */
                    color: white; /* White text color */
                    padding: 15px 32px; /* Padding for the button */
                    text-align: center; /* Center the text horizontally */
                    text-decoration: none; /* Remove underline from the text */
                    font-size: 16px; /* Font size for the text */
                    border: none; /* Remove the default button border */
                    border-radius: 4px; /* Rounded corners */
                }

                QPushButton:hover {
                    background-color: #45a049; /* Darker green color on hover */
                }

                QPushButton:pressed {
                    background-color: #367c39; /* Even darker green color on button press */
                }
            """
        self.fButton.setStyleSheet(style)
        self.cButton.setStyleSheet(style)
        self.sButton.setStyleSheet(style)
        
        self.setLayout(layout)
    def scan_license(self):
        self.license_plate_result = detect_plate()
        if(self.license_plate_result != None):
            QMessageBox.information(self,"License Plate Successful",'Name: ' + self.license_plate_result['name']+'\n'+'Registration Number: '+self.license_plate_result['reg.no']+'\n'+'Car Number: '+self.license_plate_result['car_no'], QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
        else:
             QMessageBox.critical(self, "Error",
                                     "Unregistered Number or something went wrong.")

        


    def go_to_form(self):
        form = CSVForm()
        self.parent().setCentralWidget(form)

    def go_student_entry(self):
        self.studentEntry = StudentEntry()
        self.parent().setCentralWidget(self.studentEntry)

# class SecondUI(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         layout=QVBoxLayout()
#         self.label=QLabel("Second UI",self)
#         layout.addWidget(self.label)
#
#         self.button = QPushButton("Go to first ui", self)
#         self.button.clicked.connect(self.switch_to_first_ui)
#         layout.addWidget(self.button)
#
#         self.setLayout(layout)
#
#     def switch_to_first_ui(self):
#         first_ui = Home()
#         self.parent().setCentralWidget(first_ui)

class CSVForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.regNo_label = QLabel("Register No")
        self.regNo_input = QLineEdit()
        self.regNo_input.setPlaceholderText("UIT0000")

        self.carNo_label = QLabel("Car No (optional)" )
        self.carNo_input = QLineEdit()
        self.carNo_input.setPlaceholderText("1A0000")

        self.image_label = QLabel()

        self.choose_button = QPushButton("Choose Image" , self)
        self.choose_button.clicked.connect(self.choose_image)

        self.save_button = QPushButton("Save to CSV", self)
        self.save_button.clicked.connect(self.save_to_csv)

        self.fButton = QPushButton("Back To Home", self)
        self.fButton.clicked.connect(self.go_to_home)

        self.setStyleSheet(
            """
            background-color: #f0f0f0;
            """
        )

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.regNo_label)
        layout.addWidget(self.regNo_input)
        layout.addWidget(self.carNo_label)
        layout.addWidget(self.carNo_input)
        layout.addWidget(self.image_label)
        layout.addWidget(self.choose_button)

        layout.addWidget(self.save_button)
        layout.addWidget(self.fButton)

        self.setLayout(layout)

    image_path = None

    def go_to_home(self):
        home = Home()
        self.parent().setCentralWidget(home)

    def choose_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose Image File", "", "Image Files (*.png *.jpg *.jpeg *.gif);;All Files (*)",
            options=QFileDialog.Option.ReadOnly
        )

        if file_name:
            self.image_path = file_name
            cv_image = cv2.imread(self.image_path)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            height, width, channel = cv_image.shape
            bytes_per_line = channel * width
            q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

            self.image_pixmap = QPixmap.fromImage(q_image)

            # image = self.image_pixmap.toImage()
            # width, height = image.width(), image.height()
            # buffer = image.constBits()
            # self.np_image = np.frombuffer(buffer,np.uint8).reshape((height,width,4))

            self.image_label.setPixmap(
                self.image_pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.save_button.setEnabled(True)

    def save_to_csv(self):
        name = self.name_input.text()
        regNo = self.regNo_input.text()
        carNo = self.carNo_input.text()
        regNoExist = False
        carNoExist = False
        # results = mp_face_detection.process(self.np_image)
        if carNo:
            if re.match("^\d[A-Z]\d{4}$",carNo):
                carNoMatch = True
            else:
                carNoMatch = False
        else:
            carNo=''

        id = 0
        with open("data.csv", encoding='utf-8', mode='r') as file:
            csvReader = csv.DictReader(file)
            for rows in csvReader:
                car_no = rows['car_no']
                reg_no = rows['reg.no']
                if(car_no== carNo and car_no !=''):
                    carNoExist = True
                if(reg_no == regNo):
                    regNoExist = True
                id += 1
        
        carNoMatch = True

        

        if self.image_path is None:
                QMessageBox.critical(self, "Error",
                                     "No Image is selected")
                return 
        elif carNoExist == True:
            QMessageBox.critical(self, "Error",
                                     "Car No already exists")
            return 
        
        elif regNoExist == True:
            QMessageBox.critical(self, "Error",
                                     "Registration Number already exists")
            return 

        else:
            options = QFileDialog.Option.ReadOnly
            default_name = regNo
            if name and regNo:
                if not re.match("^UIT\d{4}$",regNo) and carNoMatch:
                    QMessageBox.critical(self, "Error","Wrong input value format")
                # if results.detection:
                else:
                    cv_image = cv2.imread(self.image_path)
                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                    results = mp_face_detection.process(cv_image)
                    if results.detections:
                        new_file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "./faces/" + default_name,
                                                            "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                            options=options)
                        self.image_pixmap.save(new_file_name)
                        with open("data.csv", encoding='utf-8', mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([id + 1, name, regNo, carNo, default_name + os.path.splitext(new_file_name)[1]])
                        QMessageBox.information(self,"Successful","Successfully registered user", QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
                        self.name_input.clear()
                        self.regNo_input.clear()
                        self.carNo_input.clear()
                        self.image_label.clear()
                        self.new_file_name = None
                    else:
                        QMessageBox.critical(self, "Error", "No face detected in the image")


            else:
                QMessageBox.critical(self, "Error", "All required fields are not filled")



class StudentEntry(QWidget):

    qr_result = ''
    faceScan_result = ''
    def __init__(self):
        super().__init__()

        # self.setWindowTitle("Student Entry")
        # self.setGeometry(100, 100, 400, 300)

        # self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.button1 = QPushButton("Start Verifying")
        layout.addWidget(self.button1)
        self.button1.clicked.connect(self.scanCode)

        self.button3 = QPushButton("Back To Main Menu")
        layout.addWidget(self.button3)
        self.button3.clicked.connect(self.go_to_home) 

        # self.central_widget.setLayout(layout)

        style = """
                QPushButton {
                    background-color: #4CAF50; /* Green background color */
                    color: white; /* White text color */
                    padding: 15px 32px; /* Padding for the button */
                    text-align: center; /* Center the text horizontally */
                    text-decoration: none; /* Remove underline from the text */
                    font-size: 16px; /* Font size for the text */
                    border: none; /* Remove the default button border */
                    border-radius: 4px; /* Rounded corners */
                }

                QPushButton:hover {
                    background-color: #45a049; /* Darker green color on hover */
                }

                QPushButton:pressed {
                    background-color: #367c39; /* Even darker green color on button press */
                }
            """

        self.button1.setStyleSheet(style)
        self.button3.setStyleSheet(style)
        self.setLayout(layout)

    def go_to_home(self):
        home = Home()
        self.parent().setCentralWidget(home)  # Emit the custom signal

    def scanCode(self):
        fr = FaceRecognition()
        passScan = False
        while (passScan == False):
            self.qr_result = scan_qr_code()
            qrSuccess = QMessageBox(self)
            qrSuccess.setWindowTitle("QR scanned successfully")
            qrSuccess.setText('Name: ' + self.qr_result['name']+'\n'+'Registration Number: '+self.qr_result['reg.no']+ '\n'+'Please scan your face to verify and enter the campus')
            qrSuccess.setStyleSheet(
                "QMessageBox {"
                "   background-color: 	#00FF7F;"
                "   opacity: 0.6;"
                "   color: #FD3AD1;"
                "   font-size: 30px;"
                "   text-align: center;"
                "   padding: 16px 30px;"
                "}"
                 "QMessageBox QLabel {"
                "   color: #FFFFFF;"  # Change the font color to your desired color
                "   text-align: center;"
                "   margin: 10px 30px;"
                "}"
                "QMessageBox QPushButton {"
                "   background-color: #007BFF;"
                "   color: #FFFFFF;"
                "   border: none;"
                "   font-size: 30px;"
                "   border-radius: 5px;"
                "   padding: 20px 20px;"
                "   width: 100%;"
                "}"
                "QMessageBox QPushButton:hover {"
                "   background-color: #0056b3;"
                "}"
            )
            qrSuccess.exec()
            # QMessageBox.information(self,"QR verification successful",'Name: ' + self.qr_result['name']+'\n'+'Registration Number: '+self.qr_result['reg.no']+ '\n'+'Please scan your face to verify and enter the campus', QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
            self.faceScan_result = fr.run_recognition()
            if(self.qr_result['reg.no'] == self.faceScan_result['reg.no']):
                passScan = True
                Success = QMessageBox(self)
                Success.setWindowTitle("Access Granted")
                Success.setText('You may now enter the campus'+'\n'+ 'Name: ' + self.qr_result['name']+'\n'+'Registration Number: '+self.qr_result['reg.no']+ '\n')
                Success.setStyleSheet(
                "QMessageBox {"
                "   background-color: 	#00FF7F;"
                "   opacity: 0.6;"
                "   color: #FD3AD1;"
                "   font-size: 30px;"
                "   text-align: center;"
                "   padding: 16px 30px;"
                "}"
                 "QMessageBox QLabel {"
                "   color: #FFFFFF;"  # Change the font color to your desired color
                "   text-align: center;"
                "   margin: 10px 30px;"
                "}"
                "QMessageBox QPushButton {"
                "   background-color: #007BFF;"
                "   color: #FFFFFF;"
                "   border: none;"
                "   font-size: 30px;"
                "   border-radius: 5px;"
                "   padding: 20px 20px;"
                "   width: 100%;"
                "}"
                "QMessageBox QPushButton:hover {"
                "   background-color: #0056b3;"
                "}"
            )
                Success.exec()
                # QMessageBox.information(self,"Successfully verified",'You may now enter the campus'+'\n'+ 'Name: ' + self.qr_result['name']+'\n'+'Registration Number: '+self.qr_result['reg.no']+ '\n', QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
            else:
                critical_msg_box = QMessageBox(self)
                critical_msg_box.setWindowTitle("Access Denied")
                critical_msg_box.setText("Your face does not match to the owner of the card"+ self.faceScan_result['name'])
                # critical_msg_box.setIcon(QMessageBox.Icon.Critical)
                critical_msg_box.setStyleSheet(
                "QMessageBox {"
                "   background-color: #D32F2F;"
                "   opacity: 0.6;"
                "   color: #FD3AD1;"
                "   font-size: 30px;"
                "   text-align: center;"
                "   padding: 16px 30px;"
                "}"
                 "QMessageBox QLabel {"
                "   color: #FFFFFF;"  # Change the font color to your desired color
                "   text-align: center;"
                "   margin: 10px 30px;"
                "}"
                "QMessageBox QPushButton {"
                "   background-color: #B71C1C;"
                "   color: #FFFFFF;"
                "   border: none;"
                "   font-size: 30px;"
                "   border-radius: 5px;"
                "   padding: 20px 20px;"
                "   width: 100%;"
                "}"
                "QMessageBox QPushButton:hover {"
                "   background-color: #872727;"
                "}"
            )
                
                critical_msg_box.exec()
                # QMessageBox.critical(self, "Error", "Your face does not match to the owner of the card")
                passScan = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Campus Entrance Security")
        self.setGeometry(500,300,500,500)
        home = Home()
        self.setCentralWidget(home)
    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

