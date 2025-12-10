#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件处理模块，负责文件选择、文件夹遍历和文件信息获取

该模块提供了一系列用于处理图片文件的工具函数，包括：
- 选择单个或多个图片文件
- 选择文件夹并遍历其中的图片文件
- 验证文件和文件夹的有效性
- 获取文件信息
- 检查文件格式是否支持

支持的图片格式：
- .jpg
- .jpeg
- .png
- .webp
"""
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class FileHandler:
    """文件处理类，负责文件选择、文件夹遍历和拖拽处理"""
    
    def __init__(self):
        """初始化文件处理器，设置支持的图片格式"""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
    
    def select_files(self, root=None, multiple=True):
        """选择单个或多个图片文件
        
        Args:
            root: Tkinter根窗口对象，用于显示文件选择对话框
            multiple: 是否允许选择多个文件，默认为True
            
        Returns:
            list: 选中的文件路径列表
        """
        file_types = [
            ("图片文件", "*.jpg *.jpeg *.png *.webp"),
            ("所有文件", "*.*")
        ]
        
        if root is None:
            root = tk.Tk()
            root.withdraw()
        
        if multiple:
            file_paths = filedialog.askopenfilenames(
                title="选择图片文件",
                filetypes=file_types
            )
            return list(file_paths)
        else:
            file_path = filedialog.askopenfilename(
                title="选择一个图片文件",
                filetypes=file_types
            )
            return [file_path] if file_path else []
    
    def select_folder(self, root=None):
        """选择文件夹
        
        Args:
            root: Tkinter根窗口对象，用于显示文件夹选择对话框
            
        Returns:
            str or None: 选中的文件夹路径，如果用户取消则返回None
        """
        if root is None:
            root = tk.Tk()
            root.withdraw()
        
        folder_path = filedialog.askdirectory(
            title="选择包含图片的文件夹"
        )
        return folder_path if folder_path else None
    
    def get_image_files(self, folder_path, recursive=True):
        """获取文件夹中的所有图片文件
        
        Args:
            folder_path: 要遍历的文件夹路径
            recursive: 是否递归遍历子文件夹，默认为True
            
        Returns:
            list: 包含所有支持的图片文件路径的列表
        """
        image_files = []
        
        if not os.path.exists(folder_path):
            return image_files
        
        if recursive:
            # 递归遍历文件夹及其子文件夹
            for root_dir, _, files in os.walk(folder_path):
                for file in files:
                    if self._is_supported_image(file):
                        image_files.append(os.path.join(root_dir, file))
        else:
            # 仅遍历当前文件夹
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) and self._is_supported_image(file):
                    image_files.append(file_path)
        
        return image_files
    
    def _is_supported_image(self, file_name):
        """检查文件是否为支持的图片格式
        
        Args:
            file_name: 文件名或文件路径
            
        Returns:
            bool: 如果文件格式支持则返回True，否则返回False
        """
        ext = Path(file_name).suffix.lower()
        return ext in self.supported_formats
    
    def validate_file_path(self, file_path):
        """验证文件路径是否有效
        
        Args:
            file_path: 要验证的文件路径
            
        Returns:
            tuple: (bool, str) - 第一个元素表示是否有效，第二个元素是验证结果描述
        """
        if not os.path.exists(file_path):
            return False, "文件不存在"
        
        if not os.path.isfile(file_path):
            return False, "路径不是文件"
        
        if not self._is_supported_image(file_path):
            return False, "不支持的文件格式"
        
        return True, "有效的文件"
    
    def validate_folder_path(self, folder_path):
        """验证文件夹路径是否有效
        
        Args:
            folder_path: 要验证的文件夹路径
            
        Returns:
            tuple: (bool, str) - 第一个元素表示是否有效，第二个元素是验证结果描述
        """
        if not os.path.exists(folder_path):
            return False, "文件夹不存在"
        
        if not os.path.isdir(folder_path):
            return False, "路径不是文件夹"
        
        # 检查文件夹中是否有支持的图片文件
        image_files = self.get_image_files(folder_path, recursive=False)
        if not image_files:
            return False, "文件夹中没有找到支持的图片文件"
        
        return True, "有效的文件夹"
    
    def get_file_info(self, file_path):
        """获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            dict: 包含文件信息的字典，包括name, path, size, extension等字段；如果出错则包含error字段
        """
        try:
            file_size = os.path.getsize(file_path) / 1024  # KB
            file_name = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower()
            
            return {
                'name': file_name,      # 文件名
                'path': file_path,      # 文件完整路径
                'size': round(file_size, 2),  # 文件大小，单位KB
                'extension': file_ext   # 文件扩展名（小写）
            }
        except Exception as e:
            return {
                'error': str(e)  # 错误信息
            }
    
    def batch_get_file_info(self, file_paths):
        """批量获取文件信息
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            list: 包含多个文件信息字典的列表
        """
        file_infos = []
        for file_path in file_paths:
            file_infos.append(self.get_file_info(file_path))
        return file_infos