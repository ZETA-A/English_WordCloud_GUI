import sys
from wordcloud import WordCloud
from datetime import datetime
import json
import os
import os.path

from PyQt5.QtWidgets import QApplication, QLabel
import PyQt5
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget

LOAD_ICON = '_settings/icon.png'
LOAD_JSON = '_settings/setting.json'
SETTING_GROUP = dict()

# JSON 파일체크
if os.path.isfile(LOAD_JSON):
    print("JSON 파일이 확인되었습니다")
    pass
else:
    print("JSON 파일이 존재하지않습니다")
    print(f"{LOAD_JSON} 파일을 생성합니다")
    SETTING_GROUP["TEXT_PATH"] = "UNKNOWN"
    SETTING_GROUP["BACKGROUND_COLOR"] = "white"
    SETTING_GROUP["WIDTH"] = "1000"
    SETTING_GROUP["HEIGHT"] = "1000"
    SETTING_GROUP["FONT_PATH"] = "_settings/NanumGothic.ttf"
    SETTING_GROUP["WORD_MAX_VALUE"] = "100"
    SETTING_GROUP["FONT_MAX_SIZE"] = "300"

    with open(LOAD_JSON, 'w', encoding="utf-8") as make_file:
        json.dump(SETTING_GROUP, make_file, indent="\t")

    print(f'{LOAD_JSON} 파일생성에 성공했습니다')

with open(LOAD_JSON, 'r', encoding="utf-8") as f:
    json_data = json.load(f)


class MainWindow(QMainWindow, QThread):
    def __init__(self):
        super().__init__()

        self.setGeometry(500, 500, 284, 434)
        self.setMinimumSize(284, 340)
        self.setMaximumSize(284, 340)
        self.setWindowTitle('워드클라우더')
        self.setWindowIcon(QIcon(LOAD_ICON))

        self.textFilePathLabel = QLabel(self)
        self.textFilePathLabel.setGeometry(20, 25, 121, 21)
        self.textFilePathLabel.setText('텍스트파일 경로:')

        self.textFilePathLineEdit = QLineEdit(self)
        self.textFilePathLineEdit.setGeometry(120, 25, 151, 20)
        self.textFilePathLineEdit.setText(json_data["TEXT_PATH"])

        self.backgroundColorLabel = QLabel(self)
        self.backgroundColorLabel.setGeometry(20, 80, 81, 21)
        self.backgroundColorLabel.setText('뒷배경 색상:')

        self.backgroundColorLineEdit = QLineEdit(self)
        self.backgroundColorLineEdit.setGeometry(120, 80, 125, 21)
        self.backgroundColorLineEdit.setText(json_data["BACKGROUND_COLOR"])

        self.backgroundColorToolBtn = QToolButton(self)
        self.backgroundColorToolBtn.setGeometry(244, 80, 27, 21)
        self.backgroundColorToolBtn.setText("...")
        self.backgroundColorToolBtn.clicked.connect(self.colorSetting)

        self.xRangeLabel = QLabel(self)
        self.xRangeLabel.setGeometry(20, 110, 81, 21)
        self.xRangeLabel.setText('가로 크기:')

        self.xRangeLineEdit = QLineEdit(self)
        self.xRangeLineEdit.setGeometry(120, 110, 151, 20)
        self.xRangeLineEdit.setText(json_data["WIDTH"])

        self.yRangeLabel = QLabel(self)
        self.yRangeLabel.setGeometry(20, 140, 81, 21)
        self.yRangeLabel.setText('세로 크기:')

        self.yRangeLineEdit = QLineEdit(self)
        self.yRangeLineEdit.setGeometry(120, 140, 151, 20)
        self.yRangeLineEdit.setText(json_data["HEIGHT"])

        self.fontPathLabel = QLabel(self)
        self.fontPathLabel.setGeometry(20, 200, 81, 21)
        self.fontPathLabel.setText('폰트 경로:')

        self.fontPathLineEdit = QLineEdit(self)
        self.fontPathLineEdit.setGeometry(120, 200, 151, 20)
        self.fontPathLineEdit.setText(json_data["FONT_PATH"])

        self.maxWordLabel = QLabel(self)
        self.maxWordLabel.setGeometry(20, 230, 91, 21)
        self.maxWordLabel.setText('단어 표시 갯수:')

        self.maxWordLineEdit = QLineEdit(self)
        self.maxWordLineEdit.setGeometry(120, 230, 151, 20)
        self.maxWordLineEdit.setText(json_data["WORD_MAX_VALUE"])

        self.maxWordLenLabel = QLabel(self)
        self.maxWordLenLabel.setGeometry(20, 260, 91, 21)
        self.maxWordLenLabel.setText('최대 폰트 크기:')

        self.maxWordLenLineEdit = QLineEdit(self)
        self.maxWordLenLineEdit.setGeometry(120, 260, 151, 20)
        self.maxWordLenLineEdit.setText(json_data["FONT_MAX_SIZE"])

        self.okBtn = QPushButton(self)
        self.okBtn.setGeometry(105, 300, 75, 23)
        self.okBtn.setText('변환')
        self.okBtn.clicked.connect(self.tranceWordCloud)

        self.closeBtn = QPushButton(self)
        self.closeBtn.setGeometry(195, 300, 75, 23)
        self.closeBtn.setText('종료')
        self.closeBtn.clicked.connect(self.closeProgram)

        self.settingBtn = QPushButton(self)
        self.settingBtn.setGeometry(15, 300, 75, 23)
        self.settingBtn.setText('설정적용')
        self.settingBtn.clicked.connect(self.SaveAll)

        self.dialog = QDialog()

    def tranceWordCloud(self):
        with open(LOAD_JSON, 'r', encoding="utf-8") as f:
            json_data = json.load(f)

        now = datetime.strftime(datetime.now(), "%Y-%m-%d, %H-%M-%S")
        filename = json_data["TEXT_PATH"]
        q = open(filename, 'r', encoding='utf-8')
        news = q.read()
        print(news)

        wc = WordCloud(font_path=json_data["FONT_PATH"],
                       background_color=json_data["BACKGROUND_COLOR"],
                       width=int(json_data["WIDTH"]),
                       height=int(json_data["HEIGHT"]),
                       max_words=int(json_data["WORD_MAX_VALUE"]),
                       max_font_size=int(json_data["FONT_MAX_SIZE"]))
        wc.generate(news)
        wc.to_file(f'{now} WordCloud.png')

    def SaveAll(self):
        SETTING_GROUP["TEXT_PATH"] = self.textFilePathLineEdit.text()
        SETTING_GROUP["BACKGROUND_COLOR"] = self.backgroundColorLineEdit.text()
        SETTING_GROUP["WIDTH"] = self.xRangeLineEdit.text()
        SETTING_GROUP["HEIGHT"] = self.yRangeLineEdit.text()
        SETTING_GROUP["FONT_PATH"] = self.fontPathLineEdit.text()
        SETTING_GROUP["WORD_MAX_VALUE"] = self.maxWordLineEdit.text()
        SETTING_GROUP["FONT_MAX_SIZE"] = self.maxWordLenLineEdit.text()

        with open(LOAD_JSON, 'w', encoding="utf-8") as make_file:
            json.dump(SETTING_GROUP, make_file, indent="\t")

    def closeProgram(self):
        os._exit(1)

    @pyqtSlot()
    def colorSetting(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.backgroundColorLineEdit.setText(color.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
