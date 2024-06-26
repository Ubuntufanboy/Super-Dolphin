import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, QLineEdit, QSpinBox
from PyQt5.QtGui import QPixmap
from video_layout_app import VideoLayoutApp  # Import the main application class

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Welcome to Video Layout Designer')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        logo_label = QLabel(self)
        pixmap = QPixmap('logo.png')
        logo_label.setPixmap(pixmap.scaled(100, 100, aspectRatioMode=True))
        layout.addWidget(logo_label)

        self.canvas_width = QSpinBox(self)
        self.canvas_width.setValue(500)
        self.canvas_width.setPrefix("Canvas Width: ")
        layout.addWidget(self.canvas_width)

        self.canvas_height = QSpinBox(self)
        self.canvas_height.setValue(500)
        self.canvas_height.setPrefix("Canvas Height: ")
        layout.addWidget(self.canvas_height)

        self.background_button = QPushButton('Select Background Image', self)
        self.background_button.clicked.connect(self.select_background_image)
        layout.addWidget(self.background_button)

        self.background_image_path = QLineEdit(self)
        self.background_image_path.setPlaceholderText("No background image selected")
        layout.addWidget(self.background_image_path)

        self.dark_mode_checkbox = QCheckBox('Enable Dark Mode', self)
        layout.addWidget(self.dark_mode_checkbox)

        start_button = QPushButton('Start Designing', self)
        start_button.clicked.connect(self.start_designing)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def select_background_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Background Image', '', 'Image files (*.png *.jpg *.jpeg)')
        if file_path:
            self.background_image_path.setText(file_path)

    def start_designing(self):
        canvas_width = self.canvas_width.value()
        canvas_height = self.canvas_height.value()
        background_image_path = self.background_image_path.text()
        dark_mode = self.dark_mode_checkbox.isChecked()

        self.main_app = VideoLayoutApp(canvas_width, canvas_height, background_image_path, dark_mode)
        self.main_app.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome_screen = WelcomeScreen()
    welcome_screen.show()
    sys.exit(app.exec_())

