import langdetect

def detect_language(text):
    """
    检测语言
    """
    try:
        # Detect the language
        lang = langdetect.detect(text)
        return lang
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None