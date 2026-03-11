import sys
import os
from PySide6.QtWidgets import QApplication
from gui.window import MainWindow

if __name__ == "__main__":
    # Create the directories and empty __init__.py files
    for dir_name in ['gui', 'replay', 'data']:
        os.makedirs(dir_name, exist_ok=True)
        with open(os.path.join(dir_name, '__init__.py'), 'a') as f:
            pass

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())