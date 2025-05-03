from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit
import translate_subtitle, extract_subtitle, shutil
from app import remove_subtitles, add_subtitles
import extract_subtitle
class TranslateWindow():
    def __init__(self):
        #主窗口
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 310)
        self.window.setWindowTitle('翻译字幕')
        #翻译（从）
        self.textFrom = QPlainTextEdit(self.window)
        self.textFrom.setPlaceholderText("请输入翻译语言代码（例如：zh-CT）")
        self.textFrom.move(10, 25)
        self.textFrom.resize(150, 90)
        self.textFrom.setPlainText("zh-CT")
        #翻译（到）
        self.textTo = QPlainTextEdit(self.window)
        self.textTo.setPlaceholderText("请输入目标语言代码（例如：zh-CN）")
        self.textTo.move(159, 25)
        self.textTo.resize(150, 90)
        self.textTo.setPlainText("zh-CN")
        #选择输入文件按钮
        self.button = QPushButton('选择文件', self.window)     #选择翻译视频文件按钮
        self.button.move(380, 80)
        self.button.clicked.connect(self.selectInputFile)
        #选择输出文件按钮
        self.buttonOuput = QPushButton('选择输出位置', self.window)   #选择输出位置按钮
        self.buttonOuput.move(380, 150)
        self.buttonOuput.clicked.connect(self.selectOutputPath)
        #开始翻译按钮
        self.buttonStart = QPushButton('开始翻译', self.window)
        self.buttonStart.move(380, 220)
        self.buttonStart.clicked.connect(self.process_video)
        #文件路径定义
        self.final_video = ''
        self.input_video = ''
    def process_video(self):
        from_code = self.textFrom.toPlainText()
        to_code = self.textTo.toPlainText()
        translate_subtitle.trans_init(from_code, to_code)

        temp_video = "temp/no_subtitles.mkv"
        temp_subtitle = "temp/subtitle.srt"
        temp_converted_subtitle = "temp/converted_subtitle.srt"

        #self.input_video = extract_subtitle.select_file()
        extract_subtitle.extract_subtitles(self.input_video)
        remove_subtitles(self.input_video, temp_video) 
        translate_subtitle.translate_subtitle(temp_subtitle, temp_converted_subtitle, from_code, to_code)  
        add_subtitles(temp_video, temp_converted_subtitle, self.final_video)

        print(f"处理完成！最终文件：{self.final_video}")
        shutil.rmtree('temp')
    def selectOutputPath(self):
        self.final_video = extract_subtitle.select_file_for_gui() + "/output.mkv"
    def selectInputFile(self):
        self.input_video = extract_subtitle.select_file()
    
app = QApplication()
window = TranslateWindow()
window.window.show()
app.exec()