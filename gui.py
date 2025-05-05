from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QComboBox, QLabel
import translate_subtitle, extract_subtitle, shutil
from app import remove_subtitles, add_subtitles, show_message
import extract_subtitle
class TranslateWindow():
    def __init__(self):
        #主窗口
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 310)
        self.window.setWindowTitle('翻译字幕v0.1.3')
        #翻译（从）
        self.textFrom = QComboBox(self.window)
        self.textFrom.addItems(["zh-CN", "zh-CT", ])
        self.textFrom.move(10, 25)
        self.textFrom.resize(90, 50)
        #翻译（到）
        self.textTo = QComboBox(self.window)
        self.textTo.addItems(["zh-CN", "zh-CT", "en"])
        self.textTo.move(159, 25)
        self.textTo.resize(90, 50)
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
        #提示文本
        self.textToCode = QLabel(self.window) #翻译（从）头顶文字
        self.textToCode.setText("翻译语言代码：")
        self.textToCode.move(10, 0)
        self.textFromCode = QLabel(self.window) #翻译（到）头顶文字
        self.textFromCode.setText("翻译语言代码：")
        self.textFromCode.move(159, 0)
        '''
        self.textMentionV0 = QLabel(self.window) #v0.1.3前的提示文字
        self.textMentionV0.setText("提示：v0.1.3之前版本之前第一个提示框只可使用zh-CN")
        self.textMentionV0.move(10, 80)
        self.textMentionV0.setStyleSheet("color: red;") 
        self.textMentionV0.resize(300, 50)
        self.textMentionV1 = QLabel(self.window) #v0.1.3前的提示文字
        self.textMentionV1.setText("第二个提示框只能使用zh-CT")
        self.textMentionV1.move(10, 100)
        self.textMentionV1.setStyleSheet("color: red;") 
        self.textMentionV1.resize(300, 50) 
        #测试版独享
        '''
        self.textMentionTest = QLabel(self.window)
        self.textMentionTest.setText("测试版不代表最终品质")
        self.textMentionTest.move(340, 360)
        self.textMentionTest.setStyleSheet("color: red;") 
        self.textMentionTest.resize(300, 50) 
        #文件路径定义
        self.final_video = ''
        self.input_video = ''
    def process_video(self):
        if self.input_video == '':
            show_message('请先选择输入文件！')
            return
        if self.final_video == '':
            show_message('请先选择输出位置！')
            return
        from_code = translate_subtitle.stdIn(self.textFrom.currentText())
        to_code = translate_subtitle.stdIn(self.textTo.currentText())
        if self.blacklist(from_code, to_code):
            return
        if self.input_video[-4:] == '.ass':  #如果是.ass文件
            if from_code != 'zt' and to_code != 'zh':
                translate_subtitle.trans_init(translate_subtitle.stdIn(from_code), translate_subtitle.stdIn(to_code))
                translate_subtitle.translate_subtitle_ass(self.input_video, self.input_video, from_code, to_code)
                return
            else:
                translate_subtitle.ct2cn_ass(self.input_video, self.input_video, from_code)
                return

        translate_subtitle.trans_init(translate_subtitle.stdIn(from_code), translate_subtitle.stdIn(to_code))

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
        self.final_video = extract_subtitle.select_file_for_gui(self.input_video[:-4], self.input_video[-4:])  #选择输出文件夹
    def selectInputFile(self):
        self.input_video = extract_subtitle.select_file()   #选择输入文件
    def blacklist(self, from_code, to_code):
        if from_code == to_code:
            show_message('翻译语言代码不能相同！')
            return True
        if from_code == 'zh' and to_code == 'zt':
            show_message('暂不支持繁体转简体， 请使用其他语言')
            return True
    
        
app = QApplication()
window = TranslateWindow()
window.window.show()
app.exec()