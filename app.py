#工具类
import ffmpeg
from pymkv import MKVFile
import os
import shutil
import tkinter as tk
from tkinter import messagebox
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

def add_subtitles(video_file, subtitle_file, output_file, back=False):
    """
    使用 pymkv 将 SRT 字幕封装进 MKV 的字幕轨道
    :param video_file: 无字幕的 MKV 文件
    :param subtitle_file: 需要添加的 SRT 字幕文件
    :param output_file: 输出的 MKV 文件
    :back: 是否将输出视频移动到原视频位置
    """
    mkv = MKVFile(video_file)

    # 添加字幕轨道
    mkv.add_track(subtitle_file)

    # 保存为新文件
    mkv.mux(output_file)
    print(f"✅ 成功添加字幕轨道：{output_file}")
    
    # 删除其他临时文件
    if os.path.exists(subtitle_file):
        os.remove(subtitle_file)  # 删除字幕文件
        print(f"删除了临时文件：{subtitle_file}")
    if os.path.exists(video_file):
        os.remove(video_file)  # 删除原视频文件
        print(f"删除了临时文件：{video_file}")
    if back:
        # 移动输出视频到原位置（如果需要）
        original_video_dir = os.path.dirname(video_file)  # 获取原视频所在文件夹路径
        final_video_name = os.path.basename(output_file)  # 获取输出视频的文件名
        final_video_path = os.path.join(original_video_dir, final_video_name)

        shutil.move(output_file, final_video_path)  # 移动输出视频到原位置
        print(f"✅ 输出视频已移动到原位置：{final_video_path}")
def show_message(message="暂不支持", title="提示"):
    """弹窗提示函数
    
    Parameters:
    message (str): 要显示的信息内容，默认"暂不支持 Python"
    title (str): 窗口标题，默认"提示"
    """
    # 创建临时隐藏窗口
    temp_root = tk.Tk()
    temp_root.withdraw()
    
    # 显示信息对话框
    messagebox.showinfo(title, message)
    
    # 立即销毁临时窗口
    temp_root.destroy()