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
        self.window.setWindowTitle('翻译字幕v0.1.5-pre1')
        #翻译（从）
        self.textFrom = QComboBox(self.window)
        # 创建包含显示文本和对应值的元组列表
        languages = [
            ("简体中文", "zh"),
            ("繁体中文", "zt"),
            ("英文", "en"),
            ("日文", "ja")
        ]
        # 添加带显示文本和数据的选项
        for text, data in languages:
            self.textFrom.addItem(text, data)
        self.textFrom.move(10, 25)
        self.textFrom.resize(90, 50)
        #翻译（到）
        self.textTo = QComboBox(self.window)
        # 创建包含显示文本和对应值的元组列表
        languages = [
            ("简体中文", "zh"),
            ("繁体中文", "zt"),
            ("英文", "en"),
            ("日文", "ja")
        ]

        # 添加带显示文本和数据的选项
        for text, data in languages:
            self.textTo.addItem(text, data)  # 参数1是显示文本，参数2是关联数据

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
        #提取字幕按钮
        self.buttonExtract = QPushButton('提取字幕', self.window)
        self.buttonExtract.move(380, 290)
        self.buttonExtract.clicked.connect(self.extract_subtitles)
        #自定义文本（输入）
        self.textInput = QPlainTextEdit(self.window)
        self.textInput.move(10, 90)
        self.textInput.resize(300, 50)
        self.textInput.setPlaceholderText('请输入要翻译的文本')
        #自定义文本（输出）
        self.textOutput = QPlainTextEdit(self.window)
        self.textOutput.move(10, 160)
        self.textOutput.resize(300, 50)
        self.textOutput.setReadOnly(True)
        self.textOutput.setPlaceholderText('翻译文本输出')
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
        #queue功能实现
        self.queue = []
        self.textQueue = []
    def process_video(self):
        print(self.textFrom.currentData(), self.textTo.currentData())
        from_code = self.textFrom.currentData()
        to_code = self.textTo.currentData()
        if self.textInput.toPlainText() != '':  # 如果有要翻译的文本
            if self.checkText():
                cnt = 0
                self.textQueue = [(self.textFrom.currentData(), 'en'), ('en', self.textTo.currentData())]  # 添加到列队 fromCode -> en -> toCode
                for from_code, to_code in self.textQueue:
                    print(from_code, to_code)
                    if cnt == 0:
                        translate_subtitle.trans_init(from_code, to_code)
                        temp = translate_subtitle.translator(from_code, to_code, self.textInput.toPlainText())
                    if cnt == 1:
                        self.textOutput.setPlainText(translate_subtitle.translator(from_code, to_code, temp))
                        break
                    cnt += 1
                return
            elif self.checkText() == False:
                translate_subtitle.trans_init(from_code, to_code)
                self.textOutput.setPlainText(translate_subtitle.translator(from_code, to_code, self.textInput.toPlainText()))
                return
            else:
                return
        if self.check():
            return
        if self.input_video[-4:] == '.ass':  #如果是.ass文件
            if from_code != 'zt' and to_code != 'zh':
                translate_subtitle.trans_init(from_code, to_code)
                translate_subtitle.translate_subtitle_ass(self.input_video, self.input_video, from_code, to_code)
                return
            else:
                translate_subtitle.ct2cn_ass(self.input_video, self.input_video, from_code)
                return
        if self.input_video[-4:] == '.srt':  #如果是.srt文件
            translate_subtitle.trans_init(translate_subtitle.stdIn(from_code), translate_subtitle.stdIn(to_code))
            translate_subtitle.translate_subtitle(self.input_video, self.input_video, from_code, to_code)
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
        self.final_video = extract_subtitle.select_file_for_gui(defaultFile = self.input_video.split('/')[-1][:-4], intitialExt = self.input_video[-3:])  #选择输出文件夹
    def selectInputFile(self):
        self.input_video = extract_subtitle.select_file()   #选择输入文件
    def blacklist(self):
        if self.textTo == 'en' or self.textFrom == 'en':
            return False
        whiteList = [('zt', 'zh'),
                     ('zh', 'en'),
                     ('zt', 'en'),
                     ('en', 'ja'),
                     ('ja', 'en'),
                     ('en', 'zh'),
                     ('en', 'zt')
                     ]
        if self.textFrom.currentData() == self.textTo.currentData():
            show_message('翻译语言代码不能相同！')
            return True
        for lang_from, lang_to in whiteList:
            if self.textFrom.currentData() == lang_from and self.textTo.currentData() == lang_to:
                return False
            else:
                self.queue = [(self.textFrom.currentData(), 'en'), ('en', self.textTo.currentData())]  #添加到列队 fromCode -> en -> toCode
                print(self.queue)
                self.translateQueue()
                return False
    def checkText(self):
        if self.textTo == 'en' or self.textFrom == 'en':
            print('yes')
            return False
        whiteList = [('zt', 'zh'),
                     ('zh', 'en'),
                     ('zt', 'en'),
                     ('en', 'ja'),
                     ('ja', 'en'),
                     ('en', 'zh'),
                     ('en', 'zt')
                     ]
        if self.textFrom.currentData() == self.textTo.currentData():
            show_message('翻译语言代码不能相同！')
            return 'man'
        for lang_from, lang_to in whiteList:
            if self.textFrom.currentData() == lang_from and self.textTo.currentData() == lang_to:
                return False
        return True
    def extract_subtitles(self):
        if self.check():
            return
        extract_subtitle.extract_subtitles(self.input_video, extract_subtitle.select_file_for_gui(defaultFile = self.input_video.split('/')[-1][:-4], intitialExt = '.srt'))
    def check(self, passFile = False):
        if not passFile:
            if self.input_video == '':
                show_message('请先选择输入文件！')
                return True
            if self.final_video == '':
                show_message('请先选择输出位置！')
                return True
        if self.blacklist():
            return True
    def translateQueue(self):
        cnt = 0
        temp_video = "temp/no_subtitles.mkv"
        temp_subtitle = "temp/subtitle.srt"
        temp_converted_subtitle = "temp/converted_subtitle.srt"
        for from_code, to_code in self.queue:
            print(from_code, to_code)
            translate_subtitle.trans_init(from_code, to_code)
            if cnt == 0:
                extract_subtitle.extract_subtitles(self.input_video, queued = True)
                remove_subtitles(self.input_video, temp_video) 
            translate_subtitle.translate_subtitle(temp_subtitle, temp_converted_subtitle, from_code, to_code)
            if cnt == 1:
                add_subtitles(temp_video, temp_converted_subtitle, self.final_video)
                cnt += 1
                extract_subtitle.delTemp()
                break
            if cnt == 0:
                temp_subtitle = temp_converted_subtitle
                temp_converted_subtitle = "temp/converted_subtitle" + '_' + to_code + '_' + ".srt"  
                cnt += 1         
app = QApplication()
window = TranslateWindow()
window.window.show()
app.exec()