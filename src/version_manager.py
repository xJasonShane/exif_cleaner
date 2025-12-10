#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本管理模块，负责应用版本信息的加载、解析和比较

该模块提供了一系列用于管理应用版本信息的功能，包括：
- 加载版本信息文件
- 获取当前版本号
- 获取应用名称和描述
- 获取仓库URL
- 解析版本字符串
- 比较版本号
- 检查是否有新版本可用
- 更新版本信息文件

版本信息存储在config/version.json文件中，包含以下字段：
- version: 当前版本号
- app_name: 应用名称
- description: 应用描述
- repository: 仓库URL

该模块支持PyInstaller打包环境，能够正确处理打包后的文件路径。
"""
import json
import os
from pathlib import Path

class VersionManager:
    """版本管理类，负责应用版本信息的加载、解析和比较"""
    
    def __init__(self, version_file_path=None):
        """初始化版本管理器，加载版本信息文件
        
        Args:
            version_file_path: 版本信息文件的路径，如果为None则使用默认路径
        """
        # 处理PyInstaller打包环境
        import sys
        if hasattr(sys, '_MEIPASS'):
            # 打包后的环境，获取临时目录
            base_path = sys._MEIPASS
        else:
            # 开发环境，获取项目根目录
            base_path = str(Path(__file__).parent.parent)
        
        # 设置版本信息文件路径
        self.version_file = version_file_path or os.path.join(base_path, 'config', 'version.json')
        # 加载版本信息
        self.version_data = self._load_version_data()
    
    def _load_version_data(self):
        """加载版本信息文件
        
        Returns:
            dict: 包含版本信息的字典，如果加载失败则返回默认值
        """
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            # 如果加载失败，返回默认版本信息
            return {
                'version': '0.0.0',
                'app_name': 'EXIF Cleaner',
                'description': 'A tool to batch remove EXIF information from images',
                'repository': 'https://github.com/username/clear_exif'
            }
    
    def get_current_version(self):
        """获取当前版本号
        
        Returns:
            str: 当前应用版本号
        """
        return self.version_data.get('version', '0.0.0')
    
    def get_app_name(self):
        """获取应用名称
        
        Returns:
            str: 应用名称
        """
        return self.version_data.get('app_name', 'EXIF Cleaner')
    
    def get_description(self):
        """获取应用描述
        
        Returns:
            str: 应用描述
        """
        return self.version_data.get('description', '')
    
    def get_repository_url(self):
        """获取仓库URL
        
        Returns:
            str: 仓库URL
        """
        return self.version_data.get('repository', '')
    
    def parse_version(self, version_str):
        """解析版本字符串为数字列表
        
        Args:
            version_str: 版本字符串，格式为X.Y.Z
            
        Returns:
            list: 包含版本号各部分的数字列表，如果解析失败则返回[0, 0, 0]
        """
        try:
            return [int(part) for part in version_str.split('.')]
        except Exception:
            return [0, 0, 0]
    
    def compare_versions(self, version1, version2):
        """比较两个版本号
        
        Args:
            version1: 第一个版本号，格式为X.Y.Z
            version2: 第二个版本号，格式为X.Y.Z
        
        Returns:
            int: 比较结果
            -1: version1 < version2
            0: version1 == version2
            1: version1 > version2
        """
        v1_parts = self.parse_version(version1)
        v2_parts = self.parse_version(version2)
        
        # 确保两个版本号的长度相同，不足部分用0填充
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        # 逐位比较版本号
        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0
    
    def is_newer_version(self, remote_version):
        """检查远程版本是否比当前版本新
        
        Args:
            remote_version: 远程版本号，格式为X.Y.Z
            
        Returns:
            bool: 如果远程版本比当前版本新则返回True，否则返回False
        """
        current_version = self.get_current_version()
        return self.compare_versions(remote_version, current_version) == 1
    
    def get_version_info(self):
        """获取完整的版本信息
        
        Returns:
            dict: 包含完整版本信息的字典，包括current_version、app_name、description和repository
        """
        return {
            'current_version': self.get_current_version(),
            'app_name': self.get_app_name(),
            'description': self.get_description(),
            'repository': self.get_repository_url()
        }
    
    def update_version_file(self, new_version_data):
        """更新版本信息文件
        
        Args:
            new_version_data: 新的版本信息字典，将与现有数据合并
        
        Returns:
            bool: 更新是否成功
        """
        try:
            # 合并新的版本数据到现有数据
            self.version_data.update(new_version_data)
            # 将更新后的版本数据写入文件
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump(self.version_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            # 如果更新失败，返回False
            return False