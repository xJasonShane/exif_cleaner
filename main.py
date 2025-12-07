#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入
from src.gui import ExifCleanerGUI

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
