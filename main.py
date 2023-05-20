import sys
from PIL import Image, ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget, QGridLayout


class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Image Processor')

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.brightness_label = QLabel("Brightness", self)
        self.brightness_slider = QSlider(Qt.Horizontal, self)
        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.update_image)

        self.contrast_label = QLabel("Contrast", self)
        self.contrast_slider = QSlider(Qt.Horizontal, self)
        self.contrast_slider.setMinimum(-100)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(0)
        self.contrast_slider.valueChanged.connect(self.update_image)

        self.gamma_label = QLabel("Gamma", self)
        self.gamma_slider = QSlider(Qt.Horizontal, self)
        self.gamma_slider.setMinimum(1)
        self.gamma_slider.setMaximum(500)
        self.gamma_slider.setValue(100)
        self.gamma_slider.valueChanged.connect(self.update_image)

        layout = QGridLayout()
        layout.addWidget(self.image_label, 0, 0, 1, 2)
        layout.addWidget(self.brightness_label, 1, 0)
        layout.addWidget(self.brightness_slider, 1, 1)
        layout.addWidget(self.contrast_label, 2, 0)
        layout.addWidget(self.contrast_slider, 2, 1)
        layout.addWidget(self.gamma_label, 3, 0)
        layout.addWidget(self.gamma_slider, 3, 1)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def load_image(self, file_path):
        self.image = Image.open(file_path)
        self.update_image()

    def update_image(self):
        if self.image is not None:
            brightness = self.brightness_slider.value()
            contrast = self.contrast_slider.value() / 100.0
            gamma = self.gamma_slider.value() / 100.0

            image = self.apply_adjustments(self.image, brightness, contrast, gamma)

            qimage = ImageQt.ImageQt(image)
            pixmap = QPixmap.fromImage(qimage)
            pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    @staticmethod
    def apply_adjustments(image, brightness, contrast, gamma):
        adjusted_image = image.copy()

        width, height = adjusted_image.size

        for y in range(height):
            for x in range(width):
                r, g, b = adjusted_image.getpixel((x, y))

                new_r = ImageProcessor.clamp(r + brightness)
                new_g = ImageProcessor.clamp(g + brightness)
                new_b = ImageProcessor.clamp(b + brightness)

                new_r = ImageProcessor.clamp(int(((new_r / 255.0) - 0.5) * contrast + 0.5) * 255.0)
                new_g = ImageProcessor.clamp(int(((new_g / 255.0) - 0.5) * contrast + 0.5) * 255.0)
                new_b = ImageProcessor.clamp(int(((new_b / 255.0) - 0.5) * contrast + 0.5) * 255.0)

                new_r = ImageProcessor.clamp(int(((new_r / 255.0) ** (1.0 / gamma)) * 255.0))
                new_g = ImageProcessor.clamp(int(((new_g / 255.0) ** (1.0 / gamma)) * 255.0))
                new_b = ImageProcessor.clamp(int(((new_b / 255.0) ** (1.0 / gamma)) * 255.0))

                adjusted_image.putpixel((x, y), (new_r, new_g, new_b))

        return adjusted_image

    @staticmethod
    def clamp(value):
        return max(0, min(value, 255))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ImageProcessor()
    window.resize(800, 600)
    window.show()

    file_path = 'test.jpg'  # Replace with the actual file path of your image
    window.load_image(file_path)

    sys.exit(app.exec_())
    