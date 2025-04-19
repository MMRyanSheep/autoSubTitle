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
def install_ffmpeg():
    print("FFmpeg 未安装，正在自动安装...(预计5-10分钟)")
    # 下载 FFmpeg 官方 Windows 版
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" 
    extract_dir = r"C:\ffmpeg"

    # 下载并解压
    urllib.request.urlretrieve(ffmpeg_url, download_path)
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # 将 FFmpeg 添加到系统 PATH
    bin_path = os.path.join(extract_dir, "ffmpeg-*-essentials_build", "bin")
    os.system(f'setx PATH "%PATH%;{bin_path}"')

    print("FFmpeg 安装完成！")


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

video_path = select_file()
output_path = "subtitle.srt"
ffmpeg.input(video_path).output(output_path, codec = 'srt').run()
