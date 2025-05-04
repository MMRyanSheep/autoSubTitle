#https://www.cnblogs.com/geekbruce/articles/18361899
import argostranslate.package
import argostranslate.translate
from opencc import OpenCC
def trans_init(from_code, to_code):
    if from_code == to_code:
        print("翻译语言相同，无需翻译。")
        return
    if from_code == 'zh-CT' and to_code == 'zh-CN':
        return
    # 更新语言包索引
    argostranslate.package.update_package_index() # 注释掉这行代码，会加速变快。不然代码返回结果就较慢。

    # # 获取可用的语言包
    available_packages = argostranslate.package.get_available_packages()

    # 筛选出需要的语言包并安装
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code,
            available_packages
        )
    )
    downLoad_path = package_to_install.download()
    argostranslate.package.install_from_path(downLoad_path)

def translator(from_code, to_code, text):
    # 执行翻译
    translatedText = argostranslate.translate.translate(text, from_code, to_code)
    return translatedText

def translate_subtitle(input_file, output_file, from_code, to_code):
    if from_code == 'zh-CT' and to_code == 'zh-CN':
        ct2cn(input_file, output_file)
        return
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
            lambda x: x.code == stdIn(from_code),
            installed_languages))[0]
    to_lang = list(filter(
            lambda x: x.code == stdIn(to_code),
            installed_languages))[0]
    translation = from_lang.get_translation(to_lang)

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    converted_lines = []
    # 遍历每一行内容，进行转换
    for line in lines:
        # 如果是字幕内容行，进行转换
        if not line.strip().isdigit() and "-->" not in line and line.strip():
            converted_line = translation.translate(line)
            converted_lines.append(converted_line + "\n")
        else:
            converted_lines.append(line)
    # 输出转换后的内容到新的文件
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(converted_lines)
    print(f"字幕已翻译: {output_file}")

def ct2cn(input_file, output_file):
    opencc = OpenCC('tw2s')
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    converted_lines = []
    # 遍历每一行内容，进行转换
    for line in lines:
        # 如果是字幕内容行，进行转换
        if not line.strip().isdigit() and "-->" not in line and line.strip():
            converted_line = opencc.convert(line)
            converted_lines.append(converted_line + "\n")
        else:
            converted_lines.append(line)
    # 输出转换后的内容到新的文件
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(converted_lines)
    print(f"字幕已翻译: {output_file}")

def stdIn(code):
    if code == "zh-CT":
        return "zt"
    elif code == "zh-CN":
        return "zh"
    else:
        return code