import os
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from simple_time_card import TimeCardManager

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    time_card_manager = TimeCardManager()

    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    context.setContextProperty("timeCardManager", time_card_manager)
    engine.load(os.path.join("simple_time_card", "main.qml"))

    # QML failed to load, so exit to prevent the app from hanging
    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec_())
