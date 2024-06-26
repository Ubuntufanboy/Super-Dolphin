import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsItem, QGraphicsRectItem, QComboBox)
from PyQt5.QtGui import QPixmap, QPen, QBrush, QColor, QPainter
from PyQt5.QtCore import Qt, QRectF
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, AudioFileClip

class ResizablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, *args, **kwargs):
        super().__init__(pixmap, *args, **kwargs)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.aspect_ratio = pixmap.width() / pixmap.height()
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFocus()

    def hoverMoveEvent(self, event):
        cursor = Qt.SizeAllCursor
        if event.pos().x() > self.boundingRect().width() - 10 and event.pos().y() > self.boundingRect().height() - 10:
            cursor = Qt.SizeFDiagCursor
        self.setCursor(cursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click_pos = event.pos()
            self.original_rect = self.boundingRect()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.cursor().shape() == Qt.SizeFDiagCursor:
                new_size = event.pos()
                new_width = new_size.x()
                new_height = new_size.y()
                if new_width > 10 and new_height > 10:
                    self.prepareGeometryChange()
                    self.setPixmap(self.pixmap().scaled(new_width, new_height, Qt.KeepAspectRatio))
            else:
                super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

class DraggableTextItem(QGraphicsTextItem):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

class DraggableVideoItem(QGraphicsTextItem):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

class VideoLayoutApp(QWidget):
    def __init__(self, canvas_width, canvas_height, background_image_path, dark_mode):
        super().__init__()

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.background_image_path = background_image_path
        self.dark_mode = dark_mode

        self.elements = []
        self.background_music_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Layout Designer')
        self.setGeometry(100, 100, 1200, 900)

        self.layout = QVBoxLayout()

        self.controls_layout = QHBoxLayout()
        self.add_text_button = QPushButton('Add Text', self)
        self.add_text_button.clicked.connect(self.add_text)
        self.controls_layout.addWidget(self.add_text_button)

        self.add_image_button = QPushButton('Add Image', self)
        self.add_image_button.clicked.connect(self.add_image)
        self.controls_layout.addWidget(self.add_image_button)

        self.add_video_button = QPushButton('Add Video', self)
        self.add_video_button.clicked.connect(self.add_video)
        self.controls_layout.addWidget(self.add_video_button)

        self.add_music_button = QPushButton('Add Background Music', self)
        self.add_music_button.clicked.connect(self.add_background_music)
        self.controls_layout.addWidget(self.add_music_button)

        self.export_button = QPushButton('Export to JSON', self)
        self.export_button.clicked.connect(self.export_to_json)
        self.controls_layout.addWidget(self.export_button)

        self.generate_video_button = QPushButton('Generate Video', self)
        self.generate_video_button.clicked.connect(self.generate_video)
        self.controls_layout.addWidget(self.generate_video_button)

        self.animation_combo = QComboBox(self)
        self.animation_combo.addItem('No Animation')
        self.animation_combo.addItem('Fade In')
        self.animation_combo.addItem('Slide In')
        self.controls_layout.addWidget(self.animation_combo)

        self.layout.addLayout(self.controls_layout)

        self.scene = QGraphicsScene(0, 0, self.canvas_width, self.canvas_height)
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(QRectF(0, 0, self.canvas_width, self.canvas_height))

        # Set padding and background color
        self.padding = 50
        self.view.setStyleSheet("background-color: lightgrey;" if not self.dark_mode else "background-color: black;")
        self.scene.setBackgroundBrush(QBrush(Qt.white if not self.dark_mode else Qt.darkGray))
        self.view.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        # Draw the padding rectangle
        padding_rect = QGraphicsRectItem(-self.padding, -self.padding, 
                                         self.scene.width() + 2*self.padding, 
                                         self.scene.height() + 2*self.padding)
        padding_rect.setPen(QPen(Qt.NoPen))
        padding_rect.setBrush(QBrush(QColor(200, 200, 200)))
        self.scene.addItem(padding_rect)

        # Set background image if provided
        if self.background_image_path:
            self.set_background_image(self.background_image_path)

    def add_text(self):
        default_text = "This is a placeholder for CSV text. " * 2  # 100 characters long
        text_item = DraggableTextItem(default_text[:100])
        text_item.setPos(50, 50)
        self.scene.addItem(text_item)
        self.elements.append({
            "type": "text",
            "text": default_text[:100],
            "x": 50,
            "y": 50,
            "animation": self.animation_combo.currentText()
        })

    def add_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Image files (*.png *.jpg *.jpeg)')
        if file_path:
            pixmap = QPixmap(file_path)
            image_item = ResizablePixmapItem(pixmap)
            image_item.setPos(50, 50)
            self.scene.addItem(image_item)
            self.elements.append({
                "type": "image",
                "path": file_path,
                "x": 50,
                "y": 50,
                "animation": self.animation_combo.currentText()
            })

    def add_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Video', '', 'Video files (*.mp4 *.avi)')
        if file_path:
            video_item = DraggableVideoItem("Video: " + file_path.split('/')[-1])
            video_item.setPos(50, 50)
            self.scene.addItem(video_item)
            self.elements.append({
                "type": "video",
                "path": file_path,
                "x": 50,
                "y": 50,
                "animation": self.animation_combo.currentText()
            })

    def add_background_music(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Background Music', '', 'Audio files (*.mp3 *.wav)')
        if file_path:
            self.background_music_path = file_path
            QMessageBox.information(self, "Background Music", "Background music added successfully!")

    def export_to_json(self):
        try:
            elements = []
            for item in self.scene.items():
                if isinstance(item, DraggableTextItem):
                    elements.append({
                        "type": "text",
                        "text": item.toPlainText(),
                        "x": item.pos().x(),
                        "y": item.pos().y(),
                        "animation": self.animation_combo.currentText()
                    })
                elif isinstance(item, ResizablePixmapItem):
                    elements.append({
                        "type": "image",
                        "path": item.pixmap().cacheKey(),
                        "x": item.pos().x(),
                        "y": item.pos().y(),
                        "animation": self.animation_combo.currentText()
                    })
                elif isinstance(item, DraggableVideoItem):
                    elements.append({
                        "type": "video",
                        "path": item.toPlainText().split(": ")[1],
                        "x": item.pos().x(),
                        "y": item.pos().y(),
                        "animation": self.animation_combo.currentText()
                    })

            with open("layout.json", "w") as f:
                json.dump(elements, f)
            QMessageBox.information(self, "Success", "Layout exported to JSON successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def generate_video(self):
        try:
            clips = []

            for element in self.elements:
                if element["type"] == "text":
                    text_clip = TextClip(element["text"], fontsize=24, color='white', bg_color='black')
                    text_clip = text_clip.set_position((element["x"], element["y"])).set_duration(10)
                    if element["animation"] == "Fade In":
                        text_clip = text_clip.fadein(1)
                    elif element["animation"] == "Slide In":
                        text_clip = text_clip.set_start((0, 'center')).crossfadein(1)
                    clips.append(text_clip)
                elif element["type"] == "image":
                    image_clip = ImageClip(element["path"]).set_duration(10)
                    image_clip = image_clip.set_position((element["x"], element["y"]))
                    if element["animation"] == "Fade In":
                        image_clip = image_clip.fadein(1)
                    elif element["animation"] == "Slide In":
                        image_clip = image_clip.set_start((0, 'center')).crossfadein(1)
                    clips.append(image_clip)
                elif element["type"] == "video":
                    video_clip = VideoFileClip(element["path"]).set_position((element["x"], element["y"]))
                    if element["animation"] == "Fade In":
                        video_clip = video_clip.fadein(1)
                    elif element["animation"] == "Slide In":
                        video_clip = video_clip.set_start((0, 'center')).crossfadein(1)
                    clips.append(video_clip)

            final_clip = CompositeVideoClip(clips)
            if self.background_music_path:
                audio_clip = AudioFileClip(self.background_music_path).set_duration(final_clip.duration)
                final_clip = final_clip.set_audio(audio_clip)

            final_clip.write_videofile("output_video.mp4", codec='libx264', fps=24)
            QMessageBox.information(self, "Success", "Video generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def set_background_image(self, file_path):
        pixmap = QPixmap(file_path).scaled(self.canvas_width, self.canvas_height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        background_item = QGraphicsPixmapItem(pixmap)
        background_item.setZValue(-1)  # Set to the background
        self.scene.addItem(background_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    canvas_width = 500
    canvas_height = 500
    background_image_path = None
    dark_mode = False

    if len(sys.argv) > 1:
        import welcome_screen
        canvas_width, canvas_height, background_image_path, dark_mode = welcome_screen.get_initial_settings()

    window = VideoLayoutApp(canvas_width, canvas_height, background_image_path, dark_mode)
    window.show()
    sys.exit(app.exec_())

