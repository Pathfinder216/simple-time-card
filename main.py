import sys

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

import resources
from time_card import TimeCardManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    time_card_manager = TimeCardManager()

    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    context.setContextProperty("timeCardManager", time_card_manager)
    engine.load("main.qml")

    # QML failed to load, so exit to prevent the app from hanging
    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec_())
