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
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 1

            text: "3:18"
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
                }

                Button {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 1

                    text: qsTr("Clock out")
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
}
