import os
import opencc
import ffmpeg
from tkinter import messagebox
from pymkv import MKVFile
import shutil
import subprocess
import extract_subtitle
import translate_subtitle
from app import remove_subtitles
import app

def remove_subtitles(input_video, output_video):
    """
    从视频中移除所有字幕
    :param input_video: 原始视频文件
    :param output_video: 去除字幕后的视频文件
    """
    try:
        ffmpeg.input(input_video).output(output_video, vcodec="copy", acodec="copy", sn=None).run(overwrite_output=True)
        print(f"已去除字幕：{output_video}")
    except ffmpeg.Error as e:
        print(f"移除字幕失败: {e}")
def process_video():
    from_code, to_code = input("请输入翻译语言代码（例如：zh-CT）："), input("请输入目标语言代码（例如：zh-CN）：")
    translate_subtitle.trans_init(from_code, to_code)

    temp_video = "no_subtitles.mkv"
    final_video = "final_video.mkv"

    final_path = extract_subtitle.select_file()
    extract_subtitle.extract_subtitles(final_path)
    app.remove_subtitles(final_path, temp_video)  # 去除字幕，生成 no_subtitles.mkv

    # 2. 繁体转简体（已在之前实现）
    translate_subtitle.translate_subtitle("subtitle.srt", 'converted_subtitle.srt', from_code, to_code)  # 生成 converted_subtitle.srt

    # 3. 添加翻译后的字幕
    app.add_subtitles(temp_video, "converted_subtitle.srt", final_video)

    print(f"处理完成！最终文件：{final_video}")

process_video()