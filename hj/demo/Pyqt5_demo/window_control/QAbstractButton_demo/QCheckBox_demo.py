'''
@Author：洪建
@Date：2022/3/22 16:28
'''
from PyQt5 import Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QCheckBox, QVBoxLayout

'''
QCheckBox示例
'''


class QCheckBox_Demo1(QWidget):

    def __init__(self, parent=None):
        super(QCheckBox_Demo1, self).__init__(parent)

        gbox = QGroupBox('checkboxes')
        gbox.setFlat(True)

        layout = QHBoxLayout(self)
        self.checkbox1 = QCheckBox("&Checkbox1")
        self.checkbox1.setChecked(True)
        self.checkbox1.stateChanged.connect(lambda: self.btnstate(self.checkbox1))
        layout.addWidget(self.checkbox1)

        self.checkbox2 = QCheckBox("checkbox2")
        self.checkbox2.toggled.connect(lambda: self.btnstate(self.checkbox2))
        layout.addWidget(self.checkbox2)

        self.checkbox3 = QCheckBox("Checkbox3")
        self.checkbox3.setTristate(True)
        self.checkbox3.setCheckState(Qt.PartiallyChecked)
        self.checkbox3.stateChanged.connect(lambda: self.btnstate(self.checkbox3))
        layout.addWidget(self.checkbox3)

        mainlayout = QVBoxLayout(self)
        mainlayout.addWidget(gbox)

        self.setWindowTitle("CheckBxo demo")

    def btnstate(self, btn):
        chk1_status = self.checkbox1.text() + ", ischecked=" + str(self.checkbox1.isChecked()) + "checkstate=" + str(
            self.checkbox1.checkState()) + "\n"
        chk2_status = self.checkbox2.text() + ", ischecked=" + str(self.checkbox2.isChecked()) + "checkstate=" + str(
            self.checkbox2.checkState()) + "\n"
        chk3_status = self.checkbox3.text() + ", ischecked=" + str(self.checkbox3.isChecked()) + "checkstate=" + str(
            self.checkbox3.checkState()) + "\n"
        print(chk1_status)
