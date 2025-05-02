from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit
import translate_subtitle, extract_subtitle
from app import remove_subtitles, add_subtitles
class TranslateWindow():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 310)
        self.window.setWindowTitle('翻译字幕')
        self.textFrom = QPlainTextEdit(self.window)
        self.textFrom.setPlaceholderText("请输入翻译语言代码（例如：zh-CT）")
        self.textFrom.move(10, 25)
        self.textFrom.resize(150, 90)
        self.textTo = QPlainTextEdit(self.window)
        self.textTo.setPlaceholderText("请输入目标语言代码（例如：zh-CN）")
        self.textTo.move(159, 25)
        self.textTo.resize(150, 90)
        self.button = QPushButton('选择文件', self.window)
        self.button.move(380, 80)
        self.button.clicked.connect(self.process_video)
        
    def process_video(self):
        from_code = self.textFrom.toPlainText()
        to_code = self.textTo.toPlainText()
        translate_subtitle.trans_init(from_code, to_code)

        temp_video = "no_subtitles.mkv"
        final_video = "final_video.mkv"

        final_path = extract_subtitle.select_file()
        extract_subtitle.extract_subtitles(final_path)
        remove_subtitles(final_path, temp_video) 
        translate_subtitle.translate_subtitle("subtitle.srt", 'converted_subtitle.srt', from_code, to_code)  
        add_subtitles(temp_video, "converted_subtitle.srt", final_video)

        print(f"处理完成！最终文件：{final_video}")
app = QApplication()
window = TranslateWindow()
window.window.show()
app.exec()