#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXIF Cleaner 应用入口程序

该文件是EXIF Cleaner应用的主入口点，负责：
1. 设置Python路径，确保能够正确导入项目模块
2. 创建Tkinter主窗口
3. 初始化应用程序GUI
4. 启动应用程序主循环

使用方法：
    python main.py

应用功能：
- 批量删除图片EXIF信息
- 支持多种图片格式（JPG, JPEG, PNG, WEBP）
- 提供简洁直观的GUI界面
- 支持选择性删除特定EXIF标签
- 支持创建副本后处理，不修改原始文件
- 支持检查软件更新

技术栈：
- Python 3.8+
- tkinter（GUI框架）
- piexif（EXIF处理）
- Pillow（图片处理）
- requests（网络请求）
"""
import tkinter as tk
import sys
import os

# 添加项目根目录到Python路径，确保模块能够被正确导入
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入，导入GUI应用类
from src.gui import ExifCleanerGUI

def main():
    """主程序入口函数
    
    该函数负责创建Tkinter主窗口，初始化应用程序，并启动主循环。
    """
    # 创建Tkinter主窗口
    root = tk.Tk()
    
    # 初始化应用程序，传入主窗口对象
    app = ExifCleanerGUI(root)
    
    # 运行应用程序主循环，处理用户交互事件
    app.run()

if __name__ == "__main__":
    # 当直接运行该文件时，执行主函数
    main()
