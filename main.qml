import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

ApplicationWindow {
    title: qsTr("Simple Time Card")
    width: 1280
    height: 720
    visible: true

    ColumnLayout {
        anchors.fill: parent

        Text {
            function formatTime(totalMinutes) {
                const hours = Math.floor(totalMinutes / 60)
                const minutes = totalMinutes % 60
                return hours + ":" + pad(minutes)
            }

            function pad(number) {
                return (number < 10) ? "0" + number : number
            }

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 1

            text: formatTime(minuteTimer.totalMinutes)
            fontSizeMode: Text.Fit
            font.pointSize: 128
            minimumPointSize: 8
            horizontalAlignment: Qt.AlignHCenter
            verticalAlignment: Qt.AlignVCenter
        }

        RowLayout {
            Layout.preferredHeight: 2

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 1
            }

            ColumnLayout {
                Layout.preferredWidth: 1

                Button {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 1

                    text: qsTr("Clock in")
                    enabled: !minuteTimer.running

                    onClicked: minuteTimer.start()
                }

                Button {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 1

                    text: qsTr("Clock out")
                    enabled: minuteTimer.running

                    onClicked: minuteTimer.stop()
                }

                Text {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 1

                    text: "Total: 42:19"
                    fontSizeMode: Text.Fit
                    font.pointSize: 48
                    minimumPointSize: 8
                    horizontalAlignment: Qt.AlignHCenter
                    verticalAlignment: Qt.AlignVCenter
                }
            }
        }
    }

    Timer {
        id: minuteTimer

        property int totalMinutes: 0

        // One minute
        interval: 60000

        repeat: true
        triggeredOnStart: true

        onTriggered: totalMinutes++

        onRunningChanged: {
            if (!running) {
                totalMinutes = 0
            }
        }
    }
}
