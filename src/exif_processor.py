#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import piexif
from PIL import Image
import os

class ExifProcessor:
    """EXIF信息处理核心类"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
    
    def has_exif(self, file_path):
        """检查图片是否包含EXIF信息"""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                exif_dict = piexif.load(file_path)
                # 检查是否有实际的EXIF数据（排除空字典）
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
        """获取图片的EXIF信息"""
        _, ext = os.path.splitext(file_path.lower())
        exif_info = {}
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                exif_dict = piexif.load(file_path)
                for ifd in exif_dict:
                    if ifd != 'thumbnail':
                        for tag in exif_dict[ifd]:
                            tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                            exif_info[tag_name] = exif_dict[ifd][tag]
            except Exception as e:
                exif_info['error'] = str(e)
        elif ext == '.png':
            try:
                img = Image.open(file_path)
                exif_data = img.info.get('exif')
                if exif_data:
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
        """删除图片所有EXIF信息"""
        _, ext = os.path.splitext(file_path.lower())
        output = output_path or file_path
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                with Image.open(file_path) as img:
                    img_without_exif = img.copy()
                    img_without_exif.save(output, format=img.format, quality=100, exif=b'')
                return True, None
            except Exception as e:
                return False, str(e)
        elif ext == '.png':
            try:
                with Image.open(file_path) as img:
                    img.save(output, format='PNG', exif=None)
                return True, None
            except Exception as e:
                return False, str(e)
        return False, f"不支持的格式: {ext}"
    
    def remove_selected_exif(self, file_path, tags_to_remove, output_path=None):
        """选择性删除指定的EXIF信息"""
        _, ext = os.path.splitext(file_path.lower())
        output = output_path or file_path
        
        if ext in ['.jpg', '.jpeg', '.webp']:
            try:
                with Image.open(file_path) as img:
                    exif_dict = piexif.load(img.info.get('exif') or b'')
                    
                    # 遍历所有IFD（Image File Directory）
                    for ifd in exif_dict:
                        if ifd != 'thumbnail':
                            for tag in list(exif_dict[ifd].keys()):
                                tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                                if tag_name in tags_to_remove:
                                    del exif_dict[ifd][tag]
                    
                    # 将修改后的EXIF数据写回图片
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(output, format=img.format, exif=exif_bytes, quality=100)
                return True
            except Exception as e:
                return False, str(e)
        elif ext == '.png':
            try:
                # PNG处理方式：先读取EXIF，删除指定标签，再保存
                with Image.open(file_path) as img:
                    exif_data = img.info.get('exif')
                    
                    if exif_data:
                        exif_dict = piexif.load(exif_data)
                        
                        for ifd in exif_dict:
                            if ifd != 'thumbnail':
                                for tag in list(exif_dict[ifd].keys()):
                                    tag_name = piexif.TAGS[ifd].get(tag, {}).get('name', str(tag))
                                    if tag_name in tags_to_remove:
                                        del exif_dict[ifd][tag]
                        
                        exif_bytes = piexif.dump(exif_dict)
                        img.save(output, format='PNG', exif=exif_bytes)
                    else:
                        # 如果没有EXIF数据，直接保存
                        img.save(output, format='PNG')
                
                return True
            except Exception as e:
                return False, str(e)
        return False, f"不支持的格式: {ext}"
    
    def batch_process(self, file_list, process_type='all', tags_to_remove=None, progress_callback=None):
        """批量处理图片EXIF信息"""
        results = []
        total_files = len(file_list)
        
        for index, file_path in enumerate(file_list):
            if process_type == 'all':
                result = self.remove_all_exif(file_path)
            else:
                result = self.remove_selected_exif(file_path, tags_to_remove or [])
            
            if isinstance(result, tuple):
                success, error = result
            else:
                success = result
                error = None
            
            results.append((file_path, success, error))
            
            if progress_callback and total_files > 0:
                progress = (index + 1) / total_files * 100
                progress_callback(progress)
        
        return results