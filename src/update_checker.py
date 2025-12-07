import requests
from .version_manager import VersionManager

class UpdateChecker:
    """更新检查类"""
    
    def __init__(self):
        self.version_manager = VersionManager()
        self.repository_url = self.version_manager.get_repository_url()
        self.api_url = self._get_api_url()
    
    def _get_api_url(self):
        """从仓库URL生成GitHub API URL"""
        if 'github.com' in self.repository_url:
            # 解析仓库路径，格式：https://github.com/owner/repo
            parts = self.repository_url.split('/')
            if len(parts) >= 5:
                owner = parts[-2]
                repo = parts[-1]
                return f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
        return ''
    
    def check_for_updates(self):
        """检查是否有可用更新"""
        if not self.api_url:
            return {
                'update_available': False,
                'error': 'Invalid repository URL'
            }
        
        try:
            headers = {
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get(self.api_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            release_notes = release_data.get('body', '')
            release_url = release_data.get('html_url', '')
            
            if not latest_version:
                return {
                    'update_available': False,
                    'error': 'Could not get version from GitHub release'
                }
            
            current_version = self.version_manager.get_current_version()
            update_available = self.version_manager.is_newer_version(latest_version)
            
            return {
                'update_available': update_available,
                'current_version': current_version,
                'latest_version': latest_version,
                'release_notes': release_notes,
                'release_url': release_url
            }
        except requests.RequestException as e:
            return {
                'update_available': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'update_available': False,
                'error': f'Error checking for updates: {str(e)}'
            }
    
    def get_update_info(self):
        """获取更新信息"""
        return self.check_for_updates()
    
    def is_update_available(self):
        """检查是否有更新可用，返回布尔值"""
        result = self.check_for_updates()
        return result.get('update_available', False)
    
    def get_latest_version(self):
        """获取最新版本号"""
        result = self.check_for_updates()
        return result.get('latest_version', '')
    
    def get_release_notes(self):
        """获取最新版本的发布说明"""
        result = self.check_for_updates()
        return result.get('release_notes', '')
    
    def get_release_url(self):
        """获取最新版本的发布URL"""
        result = self.check_for_updates()
        return result.get('release_url', '')