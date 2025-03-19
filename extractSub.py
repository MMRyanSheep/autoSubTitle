import os
import subprocess
import sys
import ffmpeg
import urllib.request
import zipfile
import shutil
from tkinter import Tk, filedialog, messagebox
import tkinter as tk

def check_ffmpeg():
    """检查是否安装了 ffmpeg，如果没有，尝试自动安装"""
    try:
        # 尝试执行 ffmpeg 命令，检测是否已安装
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True  # 已安装
    except FileNotFoundError:
        return False  # 未安装

def install_ffmpeg():
    """自动安装 ffmpeg（下载并解压到指定目录）"""
    try:
        # 获取系统信息，决定下载版本
        if sys.platform == "win32":
            ffmpeg_url = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-latest-win64-static.zip"
            download_dir = os.path.join(os.environ["USERPROFILE"], "ffmpeg")

            # 下载并解压 FFmpeg
            zip_file = os.path.join(download_dir, "ffmpeg.zip")
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # 下载文件
            urllib.request.urlretrieve(ffmpeg_url, zip_file)

            # 解压文件
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(download_dir)

            # 删除压缩包
            os.remove(zip_file)

            # 将 ffmpeg 路径添加到系统环境变量
            ffmpeg_bin_dir = os.path.join(download_dir, "ffmpeg-*/bin")
            os.environ["PATH"] += os.pathsep + ffmpeg_bin_dir

            messagebox.showinfo("FFmpeg 安装", "FFmpeg 已成功安装！")
        else:
            messagebox.showerror("错误", "目前仅支持 Windows 安装 FFmpeg。")
            sys.exit(1)

    except Exception as e:
        messagebox.showerror("错误", f"安装 FFmpeg 时发生错误: {str(e)}")
        sys.exit(1)

def extract_subtitles(input_video, output_srt="subtitle.srt", output_video="no_subtitles.mkv"):
    # 检查是否安装 FFmpeg
    if not check_ffmpeg():
        # 如果没有安装，则自动安装
        install_ffmpeg()

    # 获取当前程序目录
    current_directory = os.getcwd()

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
def select_file():
    """打开 Windows 文件资源管理器，选择文件"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("视频文件", "*.mkv;*.mp4;*.avi"), ("所有文件", "*.*")])
    if file_path:  # 确保用户选择了文件
        print("选择的文件路径:", file_path)
        return file_path  # 返回文件路径

final_path = select_file()
extract_subtitles(final_path)