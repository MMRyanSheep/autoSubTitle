from PyQt5.QtWidgets import QApplication, QLabel, QWidget
app = QApplication([])
window = QWidget()
label = QLabel("Hello PyQt!", parent=window)
window.show()
app.exec_()