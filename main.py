import os
import opencc
import ffmpeg
from tkinter import messagebox
from pymkv import MKVFile
import extractSub
import shutil
def convert_srt(file_path):
    """使用 OpenCC 转换 SRT 文件中的文本"""
    try:
        # 读取原始 SRT 文件
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # 创建 OpenCC 实例，进行繁体到简体转换
        converter = opencc.OpenCC('t2s')  # t2s.json：繁体到简体转换

        # 存储转换后的内容
        converted_lines = []
        
        # 遍历每一行内容，进行转换
        for line in lines:
            # 如果是字幕内容行，进行转换
            if not line.strip().isdigit() and "-->" not in line and line.strip():
                converted_line = converter.convert(line)
                converted_lines.append(converted_line + "\n")
            else:
                converted_lines.append(line)

        # 输出转换后的内容到新的文件
        output_file = os.path.join(os.getcwd(), "converted_subtitle.srt")
        with open(output_file, "w", encoding="utf-8") as file:
            file.writelines(converted_lines)

        messagebox.showinfo("转换完成", f"字幕转换完成！\n文件已保存为：{output_file}")
    except Exception as e:
        messagebox.showerror("错误", f"转换过程中发生错误: {str(e)}")

def find_srt_file():
    """查找当前目录中的 SRT 文件并进行转换"""
    current_directory = os.getcwd()

    # 查找所有 .srt 文件
    srt_files = [f for f in os.listdir(current_directory) if f.endswith(".srt")]

    if not srt_files:
        messagebox.showerror("错误", "当前目录没有找到 .srt 文件！")
        return

    # 选择第一个找到的 .srt 文件进行转换
    srt_file = srt_files[0]
    srt_file_path = os.path.join(current_directory, srt_file)

    # 调用转换函数
    convert_srt(srt_file_path)
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
def add_subtitles(video_file, subtitle_file, output_file):
    """
    使用 pymkv 将 SRT 字幕封装进 MKV 的字幕轨道
    :param video_file: 无字幕的 MKV 文件
    :param subtitle_file: 需要添加的 SRT 字幕文件
    :param output_file: 输出的 MKV 文件
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

    # 移动输出视频到原位置（如果需要）
    original_video_dir = os.path.dirname(video_file)  # 获取原视频所在文件夹路径
    final_video_name = os.path.basename(output_file)  # 获取输出视频的文件名
    final_video_path = os.path.join(original_video_dir, final_video_name)

    shutil.move(output_file, final_video_path)  # 移动输出视频到原位置
    print(f"✅ 输出视频已移动到原位置：{final_video_path}")
def process_video():
    """
    完整流程：提取字幕 + 复制视频（无字幕） -> 繁体转简体 -> 添加新字幕
    """
    temp_video = "no_subtitles.mkv"
    final_video = "final_video.mkv"

    # 1. 提取字幕 & 复制视频
    final_path = extractSub.select_file()
    extractSub.extract_subtitles(final_path)

    # 2. 繁体转简体（已在之前实现）
    convert_srt("subtitle.srt")  # 生成 converted_subtitle.srt

    # 3. 添加翻译后的字幕
    add_subtitles(temp_video, "converted_subtitle.srt", final_video)

    print(f"处理完成！最终文件：{final_video}")


# 运行程序
process_video()