#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 测试脚本，用于验证EXIF处理功能

from src.exif_processor import ExifProcessor
from src.file_handler import FileHandler


def test_exif_processor():
    """测试EXIF处理器"""
    print("=== 测试EXIF处理器 ===")
    
    processor = ExifProcessor()
    file_handler = FileHandler()
    
    # 测试图片路径（请替换为实际存在的图片路径）
    test_image = "test.jpg"  # 请替换为实际图片路径
    
    if file_handler._is_supported_image(test_image):
        print(f"测试图片: {test_image}")
        
        # 检查是否有EXIF信息
        has_exif = processor.has_exif(test_image)
        print(f"是否有EXIF信息: {has_exif}")
        
        if has_exif:
            # 获取EXIF信息
            exif_info = processor.get_exif_info(test_image)
            print(f"EXIF信息数量: {len(exif_info)}")
            print("EXIF信息:")
            for key, value in exif_info.items():
                print(f"  {key}: {value}")
            
            # 测试删除全部EXIF信息
            print("\n测试删除全部EXIF信息...")
            result = processor.remove_all_exif(test_image)
            print(f"删除结果: {result}")
            
            # 再次检查EXIF信息
            has_exif_after = processor.has_exif(test_image)
            print(f"删除后是否有EXIF信息: {has_exif_after}")
        else:
            print("该图片没有EXIF信息")
    else:
        print(f"不支持的图片格式或文件不存在: {test_image}")


if __name__ == "__main__":
    test_exif_processor()