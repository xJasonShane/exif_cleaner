#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from .file_handler import FileHandler
from .exif_processor import ExifProcessor
from .update_checker import UpdateChecker
from .version_manager import VersionManager

class ExifCleanerGUI:
    """EXIF Cleaner GUI界面"""
    
    def __init__(self, root):
        self.root = root
        
        # 设置窗口大小
        window_width = 1280
        window_height = 800
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置和大小
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        
        # 初始化组件
        self.file_handler = FileHandler()
        self.exif_processor = ExifProcessor()
        self.update_checker = UpdateChecker()
        self.version_manager = VersionManager()
        
        # 字体管理 - 统一变量，方便后续一键切换
        self.fonts = {
            'family': '微软雅黑',
            'default': ('微软雅黑', 10),
            'title': ('微软雅黑', 16, 'bold'),
            'large': ('微软雅黑', 12),
            'small': ('微软雅黑', 8),
            'bold': ('微软雅黑', 10, 'bold')
        }
        
        # 设置标题
        app_name = self.version_manager.get_app_name()
        self.root.title(f"{app_name} - EXIF清除工具")
        
        # 数据
        self.selected_files = []
        self.exif_tags_to_remove = []
        
        # EXIF标签相关
        self.all_exif_tags = self._get_all_exif_tags()  # 所有可能的EXIF标签
        self.exif_checkboxes = {}  # 存储所有EXIF标签的复选框
        self.current_image_exif = {}  # 当前选中图片的EXIF信息
        
        # 创建UI
        self._create_widgets()
    
    def _create_widgets(self):
        """创建UI组件"""
        # 为所有ttk组件设置统一字体
        style = ttk.Style()
        
        # 尝试使用系统可用的字体，确保兼容性
        try:
            # 对于中文系统，优先使用微软雅黑
            style.configure('.', font=self.fonts['default'])
            
            # 标题样式
            style.configure('Title.TLabel', font=self.fonts['title'])
            
            # 大号字体样式
            style.configure('Large.TLabel', font=self.fonts['large'])
            
            # 小号字体样式
            style.configure('Small.TLabel', font=self.fonts['small'])
            
            # 粗体样式
            style.configure('Bold.TLabel', font=self.fonts['bold'])
        except Exception as e:
            # 如果字体设置失败，使用系统默认字体
            print(f"字体设置失败: {e}")
            style.configure('.', font=('Helvetica', 10))
            style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
            style.configure('Large.TLabel', font=('Helvetica', 12))
            style.configure('Small.TLabel', font=('Helvetica', 8))
            style.configure('Bold.TLabel', font=('Helvetica', 10, 'bold'))
        
        # 添加强调按钮样式
        style.configure('Accent.TButton', foreground='#000000', background='#0078d4')
        style.map('Accent.TButton', 
                  foreground=[('pressed', '#ffffff'), ('active', '#ffffff')],
                  background=[('pressed', '#005a9e'), ('active', '#106ebe')])
        
        # 添加GitHub按钮高亮样式
        style.configure('Highlight.TButton', foreground='#000000', background='#24292e')
        style.map('Highlight.TButton',
                  foreground=[('pressed', '#ffffff'), ('active', '#ffffff')],
                  background=[('pressed', '#161b22'), ('active', '#30363d')])
        
        
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)  # 已选择文件区域现在在row=3
        main_frame.rowconfigure(4, weight=1)
        
        # 标题
        app_name = self.version_manager.get_app_name()
        version = self.version_manager.get_current_version()
        title_label = ttk.Label(main_frame, text=f"{app_name} v{version}", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 操作按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # 选择文件按钮
        self.select_file_btn = ttk.Button(button_frame, text="选择文件", command=self._select_files)
        self.select_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 选择文件夹按钮
        self.select_folder_btn = ttk.Button(button_frame, text="选择文件夹", command=self._select_folder)
        self.select_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空列表按钮
        self.clear_list_btn = ttk.Button(button_frame, text="清空列表", command=self._clear_list)
        self.clear_list_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除EXIF按钮
        self.remove_exif_btn = ttk.Button(button_frame, text="删除全部EXIF", command=self._remove_all_exif)
        self.remove_exif_btn.pack(side=tk.RIGHT, padx=5)
        
        # 检查更新按钮
        self.check_update_btn = ttk.Button(button_frame, text="检查更新", command=self._check_updates)
        self.check_update_btn.pack(side=tk.RIGHT, padx=5)
        
        # 关于按钮
        self.about_btn = ttk.Button(button_frame, text="关于", command=self._show_about_dialog)
        self.about_btn.pack(side=tk.RIGHT, padx=5)
        
        # 拖拽提示
        drag_frame = ttk.LabelFrame(main_frame, text="拖拽区域")
        drag_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        drag_frame.columnconfigure(0, weight=1)
        
        self.drag_label = ttk.Label(drag_frame, text="将图片或文件夹拖拽到此处", style='Large.TLabel')
        self.drag_label.grid(row=0, column=0, pady=20)
        
        # 文件列表框架
        file_frame = ttk.LabelFrame(main_frame, text="已选择文件")
        file_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(0, weight=1)
        
        # 文件列表
        self.file_tree = ttk.Treeview(file_frame, columns=('name', 'size', 'path'), show='headings')
        self.file_tree.heading('name', text='文件名', anchor=tk.W)
        self.file_tree.heading('size', text='大小 (KB)', anchor=tk.E)
        self.file_tree.heading('path', text='路径', anchor=tk.W)
        
        self.file_tree.column('name', width=200, anchor=tk.W)
        self.file_tree.column('size', width=100, anchor=tk.E)
        self.file_tree.column('path', width=400, anchor=tk.W)
        
        # 文件列表滚动条
        file_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=file_scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 添加文件选择事件监听器
        self.file_tree.bind('<<TreeviewSelect>>', self._on_file_select)
        
        # EXIF信息和选项框架
        exif_frame = ttk.LabelFrame(main_frame, text="EXIF选项")
        exif_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        exif_frame.columnconfigure(0, weight=1)
        exif_frame.columnconfigure(1, weight=1)
        exif_frame.rowconfigure(0, weight=1)
        
        # 左半部分：EXIF信息列表（复选框）
        info_frame = ttk.LabelFrame(exif_frame, text="EXIF信息列表")
        info_frame.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        
        # 创建内部框架放置复选框
        self.checkbox_inner_frame = ttk.Frame(info_frame)
        self.checkbox_inner_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建复选框
        self.exif_var_dict = {}
        self.create_exif_checkboxes()
        
        # 右半部分：操作按钮和说明
        options_frame = ttk.LabelFrame(exif_frame, text="操作选项")
        options_frame.grid(row=0, column=1, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        options_frame.columnconfigure(0, weight=1)
        options_frame.rowconfigure(1, weight=1)
        
        # 全选/取消全选按钮
        button_row = ttk.Frame(options_frame)
        button_row.pack(fill=tk.X, padx=5, pady=5)
        
        select_all_btn = ttk.Button(button_row, text="全选", command=self._select_all_tags)
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
        deselect_all_btn = ttk.Button(button_row, text="取消全选", command=self._deselect_all_tags)
        deselect_all_btn.pack(side=tk.LEFT, padx=5)
        
        # 当前选中图片信息
        info_text = ttk.Label(options_frame, text="说明:", style='Bold.TLabel')
        info_text.pack(anchor=tk.W, padx=5, pady=5)
        
        info_content = ttk.Label(options_frame, text="1. 勾选需要清除的EXIF信息\n2. 未勾选的EXIF信息将被保留\n3. 图片中不存在的EXIF信息会显示为未勾选\n4. 选择图片后会高亮显示该图片包含的EXIF信息", 
                                wraplength=300, justify=tk.LEFT)
        info_content.pack(anchor=tk.W, padx=5, pady=5)
        
        # 删除所选标签按钮
        remove_selected_btn = ttk.Button(options_frame, text="删除所选EXIF", command=self._remove_selected_exif)
        remove_selected_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    def _select_files(self):
        """选择文件"""
        file_paths = self.file_handler.select_files(self.root)
        self._add_files_to_list(file_paths)
    
    def _select_folder(self):
        """选择文件夹"""
        folder_path = self.file_handler.select_folder(self.root)
        if folder_path:
            file_paths = self.file_handler.get_image_files(folder_path)
            self._add_files_to_list(file_paths)
    
    def _add_files_to_list(self, file_paths):
        """将文件添加到列表"""
        for file_path in file_paths:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                file_info = self.file_handler.get_file_info(file_path)
                self.file_tree.insert('', tk.END, values=(file_info['name'], file_info['size'], file_path))
        self.status_var.set(f"已选择 {len(self.selected_files)} 个文件")
        
        # 如果只有一个文件被选择，更新EXIF信息和复选框状态
        if len(self.selected_files) == 1:
            self._update_exif_info(self.selected_files[0])
    
    def _update_exif_info(self, file_path):
        """更新EXIF信息和复选框状态"""
        # 获取当前文件的EXIF信息
        self.current_image_exif = self.exif_processor.get_exif_info(file_path)
        
        # 重置所有复选框样式
        for tag_name in self.exif_checkboxes:
            self.exif_checkboxes[tag_name].configure(style='')
        
        # 高亮显示当前文件包含的EXIF标签
        for tag_name in self.current_image_exif:
            if tag_name in self.exif_checkboxes:
                # 可以添加高亮样式，这里简单地使用加粗
                self.exif_checkboxes[tag_name].configure(style='Bold.TCheckbutton')
    
    def _clear_list(self):
        """清空文件列表"""
        self.selected_files.clear()
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.status_var.set("就绪")
        self.current_image_exif = {}
        
        # 重置所有复选框状态
        for tag_name in self.exif_var_dict:
            self.exif_var_dict[tag_name].set(False)
        
        # 重置所有复选框样式
        for tag_name in self.exif_checkboxes:
            self.exif_checkboxes[tag_name].configure(style='')
    
    def _remove_all_exif(self):
        """删除所有EXIF信息"""
        if not self.selected_files:
            messagebox.showwarning("警告", "未选择文件")
            return
        
        # 询问用户确认
        confirm = messagebox.askyesno("确认", f"确定要删除 {len(self.selected_files)} 个文件的所有EXIF信息吗？")
        if not confirm:
            return
        
        # 开始处理
        self._start_processing()
        
        # 在后台线程中处理
        def process_files():
            def update_progress(progress):
                self.progress_var.set(progress)
                self.status_var.set(f"正在处理... {int(progress)}%")
            
            results = self.exif_processor.batch_process(
                self.selected_files, 
                process_type='all',
                progress_callback=update_progress
            )
            self._finish_processing(results)
        
        threading.Thread(target=process_files, daemon=True).start()
    
    def _remove_selected_exif(self):
        """删除所选EXIF信息"""
        if not self.selected_files:
            messagebox.showwarning("警告", "未选择文件")
            return
        
        # 获取所有被勾选的EXIF标签
        selected_tags = []
        for tag_name, var in self.exif_var_dict.items():
            if var.get():
                selected_tags.append(tag_name)
        
        if not selected_tags:
            messagebox.showwarning("警告", "未选择EXIF标签")
            return
        
        # 询问用户确认
        confirm = messagebox.askyesno("确认", f"确定要从 {len(self.selected_files)} 个文件中删除所选的EXIF标签吗？")
        if not confirm:
            return
        
        # 开始处理
        self._start_processing()
        
        # 在后台线程中处理
        def process_files():
            def update_progress(progress):
                self.progress_var.set(progress)
                self.status_var.set(f"正在处理... {int(progress)}%")
            
            results = self.exif_processor.batch_process(
                self.selected_files, 
                process_type='selected',
                tags_to_remove=selected_tags,
                progress_callback=update_progress
            )
            self._finish_processing(results)
        
        threading.Thread(target=process_files, daemon=True).start()
    
    def _start_processing(self):
        """开始处理"""
        self.status_var.set("正在处理...")
        self.progress_var.set(0)
        self.select_file_btn.config(state=tk.DISABLED)
        self.select_folder_btn.config(state=tk.DISABLED)
        self.clear_list_btn.config(state=tk.DISABLED)
        self.remove_exif_btn.config(state=tk.DISABLED)
    
    def _finish_processing(self, results):
        """完成处理"""
        # 统计结果
        success_count = sum(1 for _, success, _ in results if success)
        error_count = len(results) - success_count
        
        # 更新UI
        self.root.after(0, lambda: self._update_processing_results(success_count, error_count))
    
    def _update_processing_results(self, success_count, error_count):
        """更新处理结果"""
        self.progress_var.set(100)
        self.status_var.set(f"处理完成: {success_count} 个成功, {error_count} 个失败")
        self.select_file_btn.config(state=tk.NORMAL)
        self.select_folder_btn.config(state=tk.NORMAL)
        self.clear_list_btn.config(state=tk.NORMAL)
        self.remove_exif_btn.config(state=tk.NORMAL)
        
        # 显示结果消息
        messagebox.showinfo("处理完成", f"成功处理 {success_count} 个文件, 失败 {error_count} 个")
    
    def _select_all_tags(self):
        """全选EXIF标签"""
        for tag_name in self.exif_var_dict:
            self.exif_var_dict[tag_name].set(True)
    
    def _deselect_all_tags(self):
        """取消全选EXIF标签"""
        for tag_name in self.exif_var_dict:
            self.exif_var_dict[tag_name].set(False)
    
    def _on_file_select(self, event):
        """文件选择事件处理"""
        # 获取选中的文件
        selected_items = self.file_tree.selection()
        if not selected_items:
            return
        
        # 只处理第一个选中的文件
        item = selected_items[0]
        file_path = self.file_tree.item(item, 'values')[2]
        
        # 更新EXIF信息和复选框状态
        self._update_exif_info(file_path)
    
    def _check_updates(self):
        """检查更新"""
        # 显示检查中提示
        self.status_var.set("正在检查更新...")
        
        def check():
            update_info = self.update_checker.check_for_updates()
            
            # 更新UI
            def update_ui():
                if update_info['update_available']:
                    self._show_update_message(update_info)
                else:
                    # 显示当前版本为最新版本
                    current_version = self.version_manager.get_current_version()
                    messagebox.showinfo("检查更新", f"当前版本 {current_version} 已是最新版本！")
                # 恢复状态栏
                self.status_var.set("就绪")
            
            self.root.after(0, update_ui)
        
        threading.Thread(target=check, daemon=True).start()
    
    def _show_update_message(self, update_info):
        """显示更新消息"""
        message = f"有新版本可用！\n\n当前版本: {update_info['current_version']}\n最新版本: {update_info['latest_version']}\n\n更新说明:\n{update_info['release_notes'][:200]}..." if update_info['release_notes'] else f"有新版本可用！\n\n当前版本: {update_info['current_version']}\n最新版本: {update_info['latest_version']}"
        
        if messagebox.askyesno("发现更新", message + "\n\n是否访问发布页面？"):
            import webbrowser
            webbrowser.open(update_info['release_url'])
    
    def _show_about_dialog(self):
        """显示关于对话框"""
        # 创建关于窗口
        about_window = tk.Toplevel(self.root)
        about_window.title("关于 EXIF Cleaner")
        about_window.geometry("500x400")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()  # 模态窗口
        
        # 设置窗口居中
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() - about_window.winfo_width()) // 2
        y = (about_window.winfo_screenheight() - about_window.winfo_height()) // 2
        about_window.geometry(f"500x400+{x}+{y}")
        
        # 创建主框架
        main_frame = ttk.Frame(about_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 应用名称和版本
        app_name = self.version_manager.get_app_name()
        version = self.version_manager.get_current_version()
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text=app_name, style='Title.TLabel')
        title_label.pack()
        
        version_label = ttk.Label(title_frame, text=f"版本 {version}")
        version_label.pack(pady=(5, 0))
        
        # 分割线
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # 描述区域
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(pady=10, fill=tk.X)
        
        desc_label = ttk.Label(
            desc_frame,
            text="一个用于批量删除图片EXIF信息的工具，支持多种图片格式，提供简洁直观的GUI界面。",
            wraplength=450,
            justify=tk.CENTER
        )
        desc_label.pack()
        
        # 信息区域
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=15, fill=tk.X)
        
        # 使用网格布局排列信息项
        info_frame.columnconfigure(0, weight=1, minsize=120)
        info_frame.columnconfigure(1, weight=2)
        
        # 作者信息
        author_label = ttk.Label(info_frame, text="作者:", style='Bold.TLabel')
        author_value = ttk.Label(info_frame, text="JasonShane")
        author_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        author_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 开源协议
        license_label = ttk.Label(info_frame, text="开源协议:", style='Bold.TLabel')
        license_value = ttk.Label(info_frame, text="MIT License")
        license_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        license_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 支持格式
        format_label = ttk.Label(info_frame, text="支持格式:", style='Bold.TLabel')
        format_value = ttk.Label(info_frame, text="JPG, JPEG, PNG, WEBP")
        format_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        format_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 技术栈
        tech_label = ttk.Label(info_frame, text="技术栈:", style='Bold.TLabel')
        tech_value = ttk.Label(info_frame, text="Python, tkinter, piexif, Pillow")
        tech_label.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        tech_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 添加GitHub仓库URL显示和按钮
        github_frame = ttk.Frame(main_frame)
        github_frame.pack(pady=15, fill=tk.X)
        
        # GitHub仓库URL显示
        repo_url = self.version_manager.get_repository_url()
        github_url_label = ttk.Label(github_frame, text=repo_url, foreground="#0066cc", cursor="hand2")
        github_url_label.pack(pady=5)
        
        # GitHub 仓库按钮 - 更明显的位置和样式
        github_btn = ttk.Button(
            github_frame,
            text="访问GitHub仓库",
            command=lambda: self._open_github_repo(),
            width=20
        )
        github_btn.pack(pady=10)
        
        # 关闭按钮
        close_btn = ttk.Button(
            main_frame,
            text="关闭",
            command=about_window.destroy,
            width=15
        )
        close_btn.pack(pady=20)
        
        # 底部版权信息
        copyright_label = ttk.Label(
            main_frame,
            text="© 2024 JasonShane. All rights reserved.",
            style='Small.TLabel'
        )
        copyright_label.pack(side=tk.BOTTOM, pady=10)
    
    def _open_github_repo(self):
        """打开GitHub仓库"""
        import webbrowser
        repo_url = self.version_manager.get_repository_url()
        if repo_url:
            webbrowser.open(repo_url)
        else:
            messagebox.showinfo("提示", "未配置GitHub仓库地址")
    
    def create_exif_checkboxes(self):
        """创建所有EXIF标签的复选框，使用多列显示"""
        # 清空当前复选框
        for widget in self.checkbox_inner_frame.winfo_children():
            widget.destroy()
        
        # 清空之前的变量和复选框字典
        self.exif_var_dict.clear()
        self.exif_checkboxes.clear()
        
        # 配置内部框架的列权重，增加到4列
        self.checkbox_inner_frame.columnconfigure(0, weight=1)
        self.checkbox_inner_frame.columnconfigure(1, weight=1)
        self.checkbox_inner_frame.columnconfigure(2, weight=1)
        self.checkbox_inner_frame.columnconfigure(3, weight=1)
        
        # 设置每行显示的列数，增加到4列
        columns = 4
        
        # 为每个EXIF标签创建复选框，默认全部勾选
        sorted_tags = sorted(self.all_exif_tags.items())
        total_tags = len(sorted_tags)
        
        for i, (tag_name, tag_cn) in enumerate(sorted_tags):
            var = tk.BooleanVar()
            var.set(True)  # 默认全部勾选
            
            # 创建复选框，显示中文名称
            checkbox = ttk.Checkbutton(
                self.checkbox_inner_frame,
                text=tag_cn,
                variable=var,
                onvalue=True,
                offvalue=False
            )
            
            # 计算行号和列号
            row = i // columns
            col = i % columns
            
            # 放置复选框
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=10, pady=1)  # 调整内边距
            
            # 保存变量和复选框，使用英文标签名作为键
            self.exif_var_dict[tag_name] = var
            self.exif_checkboxes[tag_name] = checkbox
    
    def _get_all_exif_tags(self):
        """获取精简的可删除EXIF标签，返回中英文对照字典"""
        # 精简的可删除EXIF信息列表，中英文对照
        common_exif_tags = {
            # GPS相关信息（隐私敏感）
            'GPSLatitude': 'GPS纬度',
            'GPSLongitude': 'GPS经度',
            'GPSAltitude': 'GPS海拔',
            'GPSDateTime': 'GPS日期时间',
            'GPSDateStamp': 'GPS日期',
            'GPSTimeStamp': 'GPS时间',
            
            # 相机和设备信息
            'Make': '相机品牌',
            'Model': '相机型号',
            'CameraOwnerName': '相机所有者',
            'BodySerialNumber': '相机序列号',
            'LensMake': '镜头品牌',
            'LensModel': '镜头型号',
            'FirmwareVersion': '固件版本',
            
            # 拍摄信息
            'DateTimeOriginal': '拍摄日期时间',
            'DateTimeDigitized': '数字化日期时间',
            
            # 其他隐私相关信息
            'Artist': '作者',
            'Copyright': '版权信息',
            'ImageDescription': '图像描述',
            'UserComment': '用户注释',
            'HostComputer': '拍摄设备',
            'Software': '处理软件',
        }
        
        return common_exif_tags
    
    def run(self):
        """运行应用"""
        self.root.mainloop()