#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXIF信息处理核心模块，负责图片EXIF信息的读取、检查和删除

该模块提供了一系列用于处理图片EXIF信息的功能，包括：
- 检查图片是否包含EXIF信息
- 获取图片的EXIF信息
- 删除图片的所有EXIF信息
- 选择性删除指定的EXIF信息
- 批量处理多张图片的EXIF信息

支持的图片格式：
- .jpg
- .jpeg
- .png
- .webp

技术依赖：
- piexif: 用于读取和操作EXIF数据
- PIL (Pillow): 用于处理图片文件
"""
import piexif
from PIL import Image
import os

class ExifProcessor:
    """EXIF信息处理核心类，提供EXIF信息的读取、检查和删除功能"""
    
    def __init__(self):
        """初始化EXIF处理器，设置支持的图片格式"""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
    
    def has_exif(self, file_path):
        """检查图片是否包含EXIF信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            bool: 如果图片包含EXIF信息则返回True，否则返回False
        """
        _, ext = os.path.splitext(file_path.lower())
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                exif_dict = piexif.load(file_path)
                # 检查是否有实际的EXIF数据（排除空字典和缩略图）
                for ifd in exif_dict:
                    if ifd != 'thumbnail' and exif_dict[ifd]:
                        return True
                return False
            except Exception:
                return False
        elif ext == '.png':
            try:
                img = Image.open(file_path)
                exif_data = img.info.get('exif')
                return exif_data is not None
            except Exception:
                return False
        return False
    
    def get_exif_info(self, file_path):
        """获取图片的EXIF信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            dict: 包含图片EXIF信息的字典，键为EXIF标签名，值为对应的值；如果出错则包含error字段
        """
        _, ext = os.path.splitext(file_path.lower())
        exif_info = {}
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                # 使用piexif加载EXIF数据
                exif_dict = piexif.load(file_path)
                # 遍历所有IFD（Image File Directory），排除缩略图
                for ifd in exif_dict:
                    if ifd != 'thumbnail':
                        for tag in exif_dict[ifd]:
                            # 获取标签的可读名称
                            tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                            exif_info[tag_name] = exif_dict[ifd][tag]
            except Exception as e:
                exif_info['error'] = str(e)
        elif ext == '.png':
            try:
                with Image.open(file_path) as img:
                    exif_data = img.info.get('exif')
                    if exif_data:
                        # PNG文件的EXIF数据需要特殊处理
                        exif_dict = piexif.load(exif_data)
                        for ifd in exif_dict:
                            if ifd != 'thumbnail':
                                for tag in exif_dict[ifd]:
                                    tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                                    exif_info[tag_name] = exif_dict[ifd][tag]
            except Exception as e:
                exif_info['error'] = str(e)
        
        return exif_info
    
    def remove_all_exif(self, file_path, output_path=None):
        """删除图片所有EXIF信息
        
        Args:
            file_path: 原始图片文件路径
            output_path: 处理后图片的保存路径，如果为None则覆盖原文件
            
        Returns:
            tuple: (bool, str) - 第一个元素表示是否成功，第二个元素是错误信息（如果失败）
        """
        _, ext = os.path.splitext(file_path.lower())
        output = output_path or file_path
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                with Image.open(file_path) as img:
                    # 创建图片副本并保存，不包含EXIF数据
                    img_without_exif = img.copy()
                    img_without_exif.save(output, format=img.format, quality=100, exif=b'')
                return True, None
            except Exception as e:
                return False, str(e)
        elif ext == '.png':
            try:
                with Image.open(file_path) as img:
                    # PNG格式通过设置exif=None来移除EXIF信息
                    img.save(output, format='PNG', exif=None)
                return True, None
            except Exception as e:
                return False, str(e)
        return False, f"不支持的格式: {ext}"
    
    def remove_selected_exif(self, file_path, tags_to_remove, output_path=None):
        """选择性删除指定的EXIF信息
        
        Args:
            file_path: 原始图片文件路径
            tags_to_remove: 要删除的EXIF标签列表
            output_path: 处理后图片的保存路径，如果为None则覆盖原文件
            
        Returns:
            tuple: (bool, str) - 第一个元素表示是否成功，第二个元素是错误信息（如果失败）
        """
        _, ext = os.path.splitext(file_path.lower())
        output = output_path or file_path
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                with Image.open(file_path) as img:
                    # 加载图片的EXIF数据
                    exif_dict = piexif.load(img.info.get('exif') or b'')
                    
                    # 遍历所有IFD（Image File Directory），排除缩略图
                    for ifd in exif_dict:
                        if ifd != 'thumbnail':
                            # 遍历所有标签，使用list()避免字典修改时的迭代错误
                            for tag in list(exif_dict[ifd].keys()):
                                # 获取标签的可读名称
                                tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                                # 如果标签在要删除的列表中，则删除
                                if tag_name in tags_to_remove:
                                    del exif_dict[ifd][tag]
                    
                    # 将修改后的EXIF数据转换为字节
                    exif_bytes = piexif.dump(exif_dict)
                    # 保存图片，写入修改后的EXIF数据
                    img.save(output, format=img.format, exif=exif_bytes, quality=100)
                return True, None
            except Exception as e:
                return False, str(e)
        elif ext == '.png':
            try:
                # PNG文件的EXIF处理方式不同
                with Image.open(file_path) as img:
                    exif_data = img.info.get('exif')
                    
                    if exif_data:
                        # 如果有EXIF数据，进行处理
                        exif_dict = piexif.load(exif_data)
                        
                        for ifd in exif_dict:
                            if ifd != 'thumbnail':
                                for tag in list(exif_dict[ifd].keys()):
                                    tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                                    if tag_name in tags_to_remove:
                                        del exif_dict[ifd][tag]
                        
                        # 将修改后的EXIF数据转换为字节
                        exif_bytes = piexif.dump(exif_dict)
                        # 保存PNG图片，写入修改后的EXIF数据
                        img.save(output, format='PNG', exif=exif_bytes)
                    else:
                        # 如果没有EXIF数据，直接保存
                        img.save(output, format='PNG')
                
                return True, None
            except Exception as e:
                return False, str(e)
        return False, f"不支持的格式: {ext}"
    
    def batch_process(self, file_list, process_type='all', tags_to_remove=None, progress_callback=None):
        """批量处理图片EXIF信息
        
        Args:
            file_list: 要处理的图片文件路径列表
            process_type: 处理类型，'all'表示删除所有EXIF信息，'selected'表示选择性删除
            tags_to_remove: 当process_type为'selected'时，要删除的EXIF标签列表
            progress_callback: 进度回调函数，接收一个0-100的进度值
            
        Returns:
            list: 包含每个文件处理结果的列表，每个元素为tuple(file_path, success, error)
        """
        results = []
        total_files = len(file_list)
        
        for index, file_path in enumerate(file_list):
            # 根据处理类型调用不同的处理方法
            if process_type == 'all':
                # 删除所有EXIF信息
                result = self.remove_all_exif(file_path)
            else:
                # 选择性删除指定的EXIF信息
                result = self.remove_selected_exif(file_path, tags_to_remove or [])
            
            # 处理返回结果
            if isinstance(result, tuple):
                success, error = result
            else:
                success = result
                error = None
            
            # 保存处理结果
            results.append((file_path, success, error))
            
            # 调用进度回调函数，更新处理进度
            if progress_callback and total_files > 0:
                progress = (index + 1) / total_files * 100
                progress_callback(progress)
        
        return results