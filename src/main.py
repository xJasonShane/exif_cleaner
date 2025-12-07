import tkinter as tk
from .gui import ExifCleanerGUI
import sys


def main():
    """主程序入口"""
    # 创建主窗口
    root = tk.Tk()
    
    # 初始化应用
    app = ExifCleanerGUI(root)
    
    # 运行应用
    app.run()


if __name__ == "__main__":
    main()