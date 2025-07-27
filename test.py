import pyperclip
import time


def test(self):
        last_text = ""
        while True:
            text = pyperclip.paste()
            if text != last_text:
                last_text = text
                print(f"📋 Copied: {text}")
            time.sleep(0.5)