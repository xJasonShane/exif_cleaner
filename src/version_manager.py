#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

class VersionManager:
    """版本管理类"""
    
    def __init__(self, version_file_path=None):
        self.version_file = version_file_path or os.path.join(
            Path(__file__).parent.parent, 'config', 'version.json'
        )
        self.version_data = self._load_version_data()
    
    def _load_version_data(self):
        """加载版本信息文件"""
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {
                'version': '0.0.0',
                'app_name': 'EXIF Cleaner',
                'description': 'A tool to batch remove EXIF information from images',
                'repository': 'https://github.com/username/clear_exif'
            }
    
    def get_current_version(self):
        """获取当前版本号"""
        return self.version_data.get('version', '0.0.0')
    
    def get_app_name(self):
        """获取应用名称"""
        return self.version_data.get('app_name', 'EXIF Cleaner')
    
    def get_description(self):
        """获取应用描述"""
        return self.version_data.get('description', '')
    
    def get_repository_url(self):
        """获取仓库URL"""
        return self.version_data.get('repository', '')
    
    def parse_version(self, version_str):
        """解析版本字符串为数字列表"""
        try:
            return [int(part) for part in version_str.split('.')]
        except Exception:
            return [0, 0, 0]
    
    def compare_versions(self, version1, version2):
        """比较两个版本号
        
        Args:
            version1: 第一个版本号
            version2: 第二个版本号
        
        Returns:
            -1: version1 < version2
            0: version1 == version2
            1: version1 > version2
        """
        v1_parts = self.parse_version(version1)
        v2_parts = self.parse_version(version2)
        
        # 确保两个版本号的长度相同
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0
    
    def is_newer_version(self, remote_version):
        """检查远程版本是否比当前版本新"""
        current_version = self.get_current_version()
        return self.compare_versions(remote_version, current_version) == 1
    
    def get_version_info(self):
        """获取完整的版本信息"""
        return {
            'current_version': self.get_current_version(),
            'app_name': self.get_app_name(),
            'description': self.get_description(),
            'repository': self.get_repository_url()
        }
    
    def update_version_file(self, new_version_data):
        """更新版本信息文件
        
        Args:
            new_version_data: 新的版本信息字典
        
        Returns:
            bool: 更新是否成功
        """
        try:
            self.version_data.update(new_version_data)
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump(self.version_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False