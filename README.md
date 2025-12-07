# EXIF Cleaner

一个用于批量删除图片EXIF信息的工具，支持多种图片格式，提供简洁直观的GUI界面。

## 功能特点

- 📁 **批量处理**：支持单文件和文件夹选择，可批量处理大量图片
- 🖱️ **拖拽支持**：支持将图片或文件夹直接拖拽到软件中
- 🎯 **选择性删除**：可选择删除特定的EXIF信息，或删除全部EXIF信息
- 📷 **多格式支持**：支持JPG、JPEG、PNG、WEBP等多种图片格式
- 🔍 **EXIF预览**：可查看图片的EXIF信息，方便选择要删除的内容
- ⏳ **进度显示**：显示处理进度，让您了解处理状态
- 🔄 **自动更新**：自动检查GitHub仓库的最新版本，提示用户更新
- 🎨 **简洁界面**：直观易用的GUI界面，操作简单

## 支持的图片格式

- ✅ JPG
- ✅ JPEG
- ✅ PNG
- ✅ WEBP

## 技术栈

- **编程语言**：Python 3.8+
- **GUI框架**：tkinter
- **EXIF处理**：piexif
- **图片处理**：Pillow
- **HTTP请求**：requests
- **开发环境**：虚拟环境

## 安装方法

### 1. 克隆仓库

```bash
git clone https://github.com/username/clear_exif.git
cd clear_exif
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 运行软件

```bash
python -m src.main
```

### 基本操作

1. **选择文件**：点击"选择文件"按钮选择单个或多个图片文件
2. **选择文件夹**：点击"选择文件夹"按钮选择包含图片的文件夹
3. **拖拽文件**：将图片或文件夹直接拖拽到拖拽区域
4. **删除全部EXIF**：点击"删除全部EXIF"按钮删除所有选中图片的EXIF信息
5. **选择性删除**：在EXIF选项中选择要删除的标签，点击"删除所选EXIF"按钮

### EXIF信息预览

在"EXIF信息预览"区域可以查看图片的EXIF信息，方便您了解图片中包含的元数据。

### 选择性删除

在"选择性删除"区域可以选择要删除的EXIF标签，支持全选和取消全选功能。

## 项目结构

```
clear_exif/
├── src/                    # 源代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── main.py             # 主程序入口
│   ├── gui.py              # GUI界面设计
│   ├── exif_processor.py   # EXIF信息处理核心逻辑
│   ├── file_handler.py     # 文件选择和处理
│   ├── version_manager.py  # 版本管理
│   └── update_checker.py   # 更新检查功能
├── config/                 # 配置目录
│   └── version.json        # 版本信息文件
├── logs/                   # 日志目录
│   └── update_log.md       # 更新日志文件
├── requirements.txt        # 项目依赖
├── .gitignore              # Git忽略文件
├── LICENSE                 # 许可证
└── README.md               # 项目说明文档
```

## 开发说明

### 模块设计

本项目采用模块化设计，各个功能模块独立，便于后续扩展和维护：

- **exif_processor.py**：处理EXIF信息的核心逻辑
- **file_handler.py**：处理文件选择和拖拽功能
- **version_manager.py**：管理版本信息
- **update_checker.py**：检查更新功能
- **gui.py**：GUI界面设计

### 版本管理

版本信息存储在`config/version.json`文件中，采用语义化版本控制。

### 更新检查

软件启动时会自动检查GitHub仓库的最新release版本，如果有更新会提示用户。

## 更新日志

详细的更新日志请查看`logs/update_log.md`文件。

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！

### 提交Issue

- 描述问题清晰详细
- 提供复现步骤
- 提供相关截图（如果适用）

### 提交Pull Request

- 确保代码风格一致
- 提供详细的更改说明
- 确保所有功能正常工作
- 测试新功能

## 许可证

本项目采用MIT许可证，详见`LICENSE`文件。

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues：https://github.com/username/clear_exif/issues
- 电子邮件：your.email@example.com

---

**EXIF Cleaner** - 让您的图片更隐私，更安全！