#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新检查模块，负责检查应用是否有可用更新

该模块提供了一系列用于检查应用更新的功能，包括：
- 从GitHub API获取最新版本信息
- 比较当前版本与最新版本
- 提供更新信息缓存机制，减少网络请求
- 获取更新信息的各种方法

技术依赖：
- requests: 用于发送HTTP请求获取GitHub API数据
- VersionManager: 用于获取当前版本信息和比较版本号

使用说明：
1. 创建UpdateChecker实例
2. 调用check_for_updates()方法检查更新
3. 根据返回结果判断是否有可用更新
4. 使用各种get_*方法获取具体的更新信息

更新检查流程：
1. 从版本管理器获取仓库URL
2. 生成对应的GitHub API URL
3. 发送HTTP请求获取最新release信息
4. 解析版本号、发布说明和发布URL
5. 比较当前版本与最新版本
6. 返回更新信息
7. 缓存结果，减少重复请求
"""
import requests
from .version_manager import VersionManager

class UpdateChecker:
    """更新检查类，负责检查应用是否有可用更新"""
    
    def __init__(self):
        """初始化更新检查器，设置版本管理器和仓库URL"""
        self.version_manager = VersionManager()
        self.repository_url = self.version_manager.get_repository_url()
        self.api_url = self._get_api_url()
        self._update_info_cache = None  # 缓存更新信息，减少网络请求
    
    def _get_api_url(self):
        """从仓库URL生成GitHub API URL
        
        Returns:
            str: GitHub API URL，如果仓库URL无效则返回空字符串
        """
        if 'github.com' in self.repository_url:
            # 解析仓库路径，格式：https://github.com/owner/repo
            parts = self.repository_url.split('/')
            if len(parts) >= 5:
                owner = parts[-2]  # 仓库所有者
                repo = parts[-1]    # 仓库名称
                return f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        return ''
    
    def check_for_updates(self):
        """检查是否有可用更新
        
        Returns:
            dict: 包含更新信息的字典，字段包括：
                - update_available: bool，是否有可用更新
                - current_version: str，当前版本号
                - latest_version: str，最新版本号
                - release_notes: str，发布说明
                - release_url: str，发布URL
                - error: str，错误信息（如果有）
        """
        # 使用缓存减少重复网络请求
        if self._update_info_cache is not None:
            return self._update_info_cache
        
        if not self.api_url:
            # API URL无效，返回错误信息
            self._update_info_cache = {
                'update_available': False,
                'error': 'Invalid repository URL'
            }
            return self._update_info_cache
        
        try:
            # 设置GitHub API请求头
            headers = {
                'Accept': 'application/vnd.github.v3+json'
            }
            # 发送GET请求获取最新release信息
            response = requests.get(self.api_url, headers=headers, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析JSON响应
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')  # 移除版本号前的'v'字符
            release_notes = release_data.get('body', '')  # 发布说明
            release_url = release_data.get('html_url', '')  # 发布页面URL
            
            if not latest_version:
                # 无法获取版本号，返回错误信息
                self._update_info_cache = {
                    'update_available': False,
                    'error': 'Could not get version from GitHub release'
                }
                return self._update_info_cache
            
            # 获取当前版本号并比较
            current_version = self.version_manager.get_current_version()
            update_available = self.version_manager.is_newer_version(latest_version)
            
            # 构建更新信息字典
            self._update_info_cache = {
                'update_available': update_available,
                'current_version': current_version,
                'latest_version': latest_version,
                'release_notes': release_notes,
                'release_url': release_url
            }
            return self._update_info_cache
        except requests.RequestException as e:
            # 网络请求异常
            self._update_info_cache = {
                'update_available': False,
                'error': f'Network error: {str(e)}'
            }
            return self._update_info_cache
        except Exception as e:
            # 其他异常
            self._update_info_cache = {
                'update_available': False,
                'error': f'Error checking for updates: {str(e)}'
            }
            return self._update_info_cache
    
    def get_update_info(self):
        """获取更新信息，同check_for_updates()
        
        Returns:
            dict: 包含更新信息的字典
        """
        return self.check_for_updates()
    
    def is_update_available(self):
        """检查是否有更新可用，返回布尔值
        
        Returns:
            bool: 是否有可用更新
        """
        result = self.check_for_updates()
        return result.get('update_available', False)
    
    def get_latest_version(self):
        """获取最新版本号
        
        Returns:
            str: 最新版本号
        """
        result = self.check_for_updates()
        return result.get('latest_version', '')
    
    def get_release_notes(self):
        """获取最新版本的发布说明
        
        Returns:
            str: 发布说明
        """
        result = self.check_for_updates()
        return result.get('release_notes', '')
    
    def get_release_url(self):
        """获取最新版本的发布URL
        
        Returns:
            str: 发布URL
        """
        result = self.check_for_updates()
        return result.get('release_url', '')