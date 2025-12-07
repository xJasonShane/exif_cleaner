#!/usr/bin/env python3
# 性能测试脚本，用于测试批量处理图片的性能

import time
from src.exif_processor import ExifProcessor
from src.file_handler import FileHandler

def test_batch_processing():
    """测试批量处理图片的性能"""
    print("=== 性能测试：批量处理图片 ===")
    
    processor = ExifProcessor()
    file_handler = FileHandler()
    
    # 创建测试图片（模拟）
    # 注意：实际测试时请替换为真实的图片路径
    test_images = [
        # 添加您的测试图片路径
        # "test1.jpg",
        # "test2.jpg",
        # "test3.jpg"
    ]
    
    if not test_images:
        print("请在test_images列表中添加测试图片路径")
        return
    
    print(f"测试图片数量: {len(test_images)}")
    
    # 测试1：删除全部EXIF信息
    print("\n测试1：删除全部EXIF信息")
    start_time = time.time()
    
    def update_progress(progress):
        print(f"  进度: {int(progress)}%")
    
    results = processor.batch_process(
        test_images, 
        process_type='all',
        progress_callback=update_progress
    )
    
    end_time = time.time()
    
    # 统计结果
    success_count = sum(1 for _, success, _ in results if success)
    error_count = len(results) - success_count
    
    print(f"  处理完成: {success_count} 成功, {error_count} 失败")
    print(f"  耗时: {end_time - start_time:.2f} 秒")
    print(f"  平均每个文件耗时: {(end_time - start_time) / len(test_images):.4f} 秒")
    
    # 测试2：选择性删除EXIF信息
    print("\n测试2：选择性删除EXIF信息")
    start_time = time.time()
    
    # 选择一些常见的EXIF标签进行删除
    tags_to_remove = [
        'DateTime',
        'DateTimeOriginal',
        'DateTimeDigitized',
        'GPSLatitude',
        'GPSLongitude',
        'GPSAltitude',
        'Make',
        'Model',
        'Software',
        'Artist',
        'Copyright'
    ]
    
    results = processor.batch_process(
        test_images, 
        process_type='selected',
        tags_to_remove=tags_to_remove,
        progress_callback=update_progress
    )
    
    end_time = time.time()
    
    # 统计结果
    success_count = sum(1 for _, success, _ in results if success)
    error_count = len(results) - success_count
    
    print(f"  处理完成: {success_count} 成功, {error_count} 失败")
    print(f"  耗时: {end_time - start_time:.2f} 秒")
    print(f"  平均每个文件耗时: {(end_time - start_time) / len(test_images):.4f} 秒")


if __name__ == "__main__":
    test_batch_processing()