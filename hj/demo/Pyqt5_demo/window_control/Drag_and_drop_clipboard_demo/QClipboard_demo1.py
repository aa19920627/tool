'''
@Author：洪建
@Date：2022/3/28 13:39
'''
import sys

from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QPixmap, QClipboard
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QApplication

'''
QClipboard（剪贴板）示例
'''


class QClipboard_Demo1(QWidget):
    def __init__(self, parent=None):
        super(QClipboard_Demo1, self).__init__(parent)
        text_copy_button = QPushButton("&Copy Text")
        text_paste_button = QPushButton("Paste &Text")
        html_copy_button = QPushButton("C&opy HTML")
        html_paste_button = QPushButton("Paste &HTML")
        image_copy_button = QPushButton("Co&py image")
        image_paste_button = QPushButton("paste &Image")

        self.text_label1 = QLabel("Original text")
        self.image_label1 = QLabel()
        self.image_label1.setPixmap(QPixmap("./wireless.png"))

        layout = QGridLayout(self)
        layout.addWidget(text_copy_button, 0, 0)
        layout.addWidget(image_copy_button, 0, 1)
        layout.addWidget(html_copy_button, 0, 2)
        layout.addWidget(text_paste_button, 1, 0)
        layout.addWidget(image_paste_button, 1, 1)
        layout.addWidget(html_paste_button, 1, 2)
        layout.addWidget(self.text_label1, 2, 0, 1, 2)
        layout.addWidget(self.image_label1, 2, 2)

        text_copy_button.clicked.connect(self.copy_text)
        text_paste_button.clicked.connect(self.paste_text)
        html_copy_button.clicked.connect(self.copy_html)
        html_paste_button.clicked.connect(self.paste_html)
        image_copy_button.clicked.connect(self.copy_image)
        image_paste_button.clicked.connect(self.paste_image)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText("I‘ve been clipped")

    def paste_text(self):
        clipboard = QApplication.clipboard()
        self.text_label1.setText(clipboard.text())

    def copy_image(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(QPixmap('./timg.jpg'))

    def paste_image(self):
        clipboard = QApplication.clipboard()
        self.image_label1.setPixmap(clipboard.pixmap())

    def copy_html(self):
        mime_data = QMimeData()
        mime_data.setHtml("<b>Bold and <font color=red>red</font></b>")
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mime_data)

    def paste_html(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasHtml():
            self.text_label1.setText(mime_data.html())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QClipboard_Demo1()
    win.show()
    sys.exit(app.exec_())
