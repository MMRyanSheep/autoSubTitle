#感谢 CoderPig的 extract_subtitle.py 提供的灵感
import os
import subprocess
import sys
import ffmpeg
import urllib.request
import zipfile
import shutil
from tkinter import Tk, filedialog, messagebox
import tkinter as tk
from pymkv import MKVFile
import time
'''

def extract_subtitles(input_video, output_srt="subtitle.srt", output_video="no_subtitles.mkv"):
    # 检查是否安装 FFmpeg
    if not check_ffmpeg():
        # 如果没有安装，则自动安装
        install_ffmpeg()

    # 获取当前程序目录
    # 输出字幕文件的路径（统一保存为 .srt 格式）
    try:
        # 1. 提取字幕
        ffmpeg.input(input_video).output(output_srt, format="srt").run(overwrite_output=True)
        print(f"字幕已提取: {output_srt}")

        # 2. 复制视频，并去掉字幕
        ffmpeg.input(input_video).output(output_video, vcodec="copy", acodec="copy", sn=None).run(overwrite_output=True)
        print(f"视频已复制（无字幕）: {output_video}")

    except ffmpeg.Error as e:
        print(f"处理失败: {e}")
'''
def select_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("视频文件", "*.mkv;*.mp4;*.avi"), ("所有文件", "*.*")])
    if file_path:  # 确保用户选择了文件
        print("选择的文件路径:", file_path)
        return file_path  # 返回文件路径
def extract_subtitles(video_path):
    if video_path:
        output_path = "subtitle.srt"
        try:
            ffmpeg.input(video_path).output(output_path, codec = 'srt').run()
            print(f"字幕已提取: {output_path}")
        except:
            print("提取字幕失败,请使用其他工具")
            sys.exit(1)