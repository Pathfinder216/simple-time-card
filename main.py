import sys

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

import resources

if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load("main.qml")

    # QML failed to load, so exit to prevent the app from hanging
    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec_())
