import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class FileHandler:
    """文件处理类，负责文件选择、文件夹遍历和拖拽处理"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
    
    def select_files(self, root=None, multiple=True):
        """选择单个或多个图片文件"""
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
        """选择文件夹"""
        if root is None:
            root = tk.Tk()
            root.withdraw()
        
        folder_path = filedialog.askdirectory(
            title="选择包含图片的文件夹"
        )
        return folder_path if folder_path else None
    
    def get_image_files(self, folder_path, recursive=True):
        """获取文件夹中的所有图片文件"""
        image_files = []
        
        if not os.path.exists(folder_path):
            return image_files
        
        if recursive:
            for root_dir, _, files in os.walk(folder_path):
                for file in files:
                    if self._is_supported_image(file):
                        image_files.append(os.path.join(root_dir, file))
        else:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) and self._is_supported_image(file):
                    image_files.append(file_path)
        
        return image_files
    
    def _is_supported_image(self, file_name):
        """检查文件是否为支持的图片格式"""
        ext = Path(file_name).suffix.lower()
        return ext in self.supported_formats
    
    def process_dropped_files(self, event, recursive=True):
        """处理拖拽的文件或文件夹"""
        dropped_files = []
        
        # 获取拖拽的文件路径
        paths = event.data.split()
        
        for path in paths:
            # 清理路径中的引号
            path = path.strip('"')
            
            if os.path.isfile(path):
                if self._is_supported_image(path):
                    dropped_files.append(path)
            elif os.path.isdir(path):
                # 处理文件夹中的图片
                folder_images = self.get_image_files(path, recursive=recursive)
                dropped_files.extend(folder_images)
        
        return dropped_files
    
    def validate_file_path(self, file_path):
        """验证文件路径是否有效"""
        if not os.path.exists(file_path):
            return False, "文件不存在"
        
        if not os.path.isfile(file_path):
            return False, "路径不是文件"
        
        if not self._is_supported_image(file_path):
            return False, "不支持的文件格式"
        
        return True, "有效的文件"
    
    def validate_folder_path(self, folder_path):
        """验证文件夹路径是否有效"""
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
        """获取文件信息"""
        try:
            file_size = os.path.getsize(file_path) / 1024  # KB
            file_name = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower()
            
            return {
                'name': file_name,
                'path': file_path,
                'size': round(file_size, 2),
                'extension': file_ext
            }
        except Exception as e:
            return {
                'error': str(e)
            }
    
    def batch_get_file_info(self, file_paths):
        """批量获取文件信息"""
        file_infos = []
        for file_path in file_paths:
            file_infos.append(self.get_file_info(file_path))
        return file_infos