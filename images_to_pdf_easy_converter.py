import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from converter import convert

class ConversionThread(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        success = convert(self.folder_path)
        self.finished.emit(success)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Images to PDF Easy Converter")
        self.setGeometry(100, 100, 400, 300)
        self.setAcceptDrops(True)
        
        self.setStyleSheet("background-color: #f0f0f0;")

        self.label = QLabel("Drag and drop folder here.", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(50, 50, 300, 100)
        self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #3498db; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(150, 170, 100, 30)
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.cancel_conversion)
        self.cancel_button.hide()

        self.setStyleSheet("""
            QPushButton#cancelButton {
                background-color: #dc7633;
                color: #ffffff;
                border: 2px solid #af601a;
                border-radius: 15px;
                font-size: 16px;
                padding: 5px 20px;
            }
            QPushButton#cancelButton:hover {
                background-color: #c0392b;
            }
        """)
        
        self.conversion_thread = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #226694; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            print("Dropped folder path:", folder_path)
            self.label.setText("Converting...")
            self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #3498db; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")
            self.cancel_button.show()
            
            if self.conversion_thread and self.conversion_thread.isRunning():
                self.conversion_thread.terminate()
                self.conversion_thread.wait()
                
            self.conversion_thread = ConversionThread(folder_path)
            self.conversion_thread.finished.connect(self.handle_conversion_finished)
            self.conversion_thread.start()
            
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #3498db; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")

    def handle_conversion_finished(self, success):
        self.cancel_button.hide()
        if success:
            self.label.setText("Success!")
            self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #2ecc71; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")
        else:
            self.label.setText("Failed!")
            self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #c0392b; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")

    def cancel_conversion(self):
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.terminate()
            self.label.setText("Canceled!")
            self.label.setStyleSheet("font-size: 16px; color: #ffffff; background-color: #dc7633; border: 2px dashed #999999; border-radius: 5px; padding: 20px;")
            self.cancel_button.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
