import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsItem, QGraphicsRectItem)
from PyQt5.QtGui import QPixmap, QPen, QBrush, QColor, QPainter
from PyQt5.QtCore import Qt, QRectF, QPointF

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
    def __init__(self):
        super().__init__()

        self.elements = []
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

        self.export_button = QPushButton('Export to JSON', self)
        self.export_button.clicked.connect(self.export_to_json)
        self.controls_layout.addWidget(self.export_button)

        self.layout.addLayout(self.controls_layout)

        self.scene = QGraphicsScene(0, 0, 1000, 800)
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(QRectF(0, 0, 1000, 800))

        # Set padding and background color
        self.padding = 50
        self.view.setStyleSheet("background-color: lightgrey;")
        self.scene.setBackgroundBrush(QBrush(Qt.white))
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

    def add_text(self):
        default_text = "This is a placeholder for CSV text. " * 2  # 100 characters long
        text_item = DraggableTextItem(default_text[:100])
        text_item.setPos(50, 50)
        self.scene.addItem(text_item)
        self.elements.append({"type": "text", "text": default_text[:100], "x": 50, "y": 50})

    def add_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select an Image', '', 'Image files (*.png *.jpg *.jpeg *.gif)')
        if file_path:
            pixmap = QPixmap(file_path)
            pixmap_item = ResizablePixmapItem(pixmap)
            pixmap_item.setPos(50, 100)
            self.scene.addItem(pixmap_item)
            self.elements.append({"type": "image", "path": file_path, "x": 50, "y": 100})

    def add_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select a Video', '', 'Video files (*.mp4 *.avi *.mov)')
        if file_path:
            video_label = DraggableVideoItem(f"Video: {file_path}")
            video_label.setPos(50, 150)
            self.scene.addItem(video_label)
            self.elements.append({"type": "video", "path": file_path, "x": 50, "y": 150})

    def export_to_json(self):
        # Update element positions based on their current locations in the scene
        for element in self.elements:
            items = self.scene.items()
            for item in items:
                if isinstance(item, DraggableTextItem) and "text" in element:
                    text = item.toPlainText()
                    if text == element["text"]:
                        element["x"] = item.pos().x()
                        element["y"] = item.pos().y()
                elif isinstance(item, ResizablePixmapItem) and "path" in element:
                    if item.pixmap().toImage() == QPixmap(element["path"]).toImage():
                        element["x"] = item.pos().x()
                        element["y"] = item.pos().y()
                elif isinstance(item, DraggableVideoItem) and "path" in element:
                    text = item.toPlainText()
                    if text == f"Video: {element['path']}":
                        element["x"] = item.pos().x()
                        element["y"] = item.pos().y()

        layout = {"elements": self.elements}
        try:
            with open('layout.json', 'w') as json_file:
                json.dump(layout, json_file, indent=4)
            QMessageBox.information(self, "Success", "Layout exported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoLayoutApp()
    window.show()
    sys.exit(app.exec_())
