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
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 初始化组件
        self.file_handler = FileHandler()
        self.exif_processor = ExifProcessor()
        self.update_checker = UpdateChecker()
        self.version_manager = VersionManager()
        
        # 设置标题
        app_name = self.version_manager.get_app_name()
        self.root.title(f"{app_name} - EXIF清除工具")
        
        # 数据
        self.selected_files = []
        self.exif_tags_to_remove = []
        
        # 创建UI
        self._create_widgets()
    
    def _create_widgets(self):
        """创建UI组件"""
        # 设置统一字体
        default_font = ('微软雅黑', 10)
        
        # 为所有ttk组件设置统一字体
        style = ttk.Style()
        style.configure('.', font=default_font)
        
        # 添加强调按钮样式
        style = ttk.Style()
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
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 标题
        app_name = self.version_manager.get_app_name()
        version = self.version_manager.get_current_version()
        title_label = ttk.Label(main_frame, text=f"{app_name} v{version}", font=('Arial', 16, 'bold'))
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
        
        # 文件列表框架
        file_frame = ttk.LabelFrame(main_frame, text="已选择文件")
        file_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
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
        
        # 拖拽提示
        drag_frame = ttk.LabelFrame(main_frame, text="拖拽区域")
        drag_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        drag_frame.columnconfigure(0, weight=1)
        
        # 设置统一字体
        default_font = ('微软雅黑', 12)
        self.drag_label = ttk.Label(drag_frame, text="将图片或文件夹拖拽到此处", font=default_font)
        self.drag_label.grid(row=0, column=0, pady=20)
        
        # EXIF信息和选项框架
        exif_frame = ttk.LabelFrame(main_frame, text="EXIF选项")
        exif_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        exif_frame.columnconfigure(0, weight=1)
        exif_frame.columnconfigure(1, weight=1)
        exif_frame.rowconfigure(0, weight=1)
        
        # 左半部分：EXIF信息预览
        info_frame = ttk.LabelFrame(exif_frame, text="EXIF信息预览")
        info_frame.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # 设置统一字体
        default_font = ('微软雅黑', 10)
        self.exif_info_text = tk.Text(info_frame, width=40, height=15, wrap=tk.WORD, font=default_font)
        self.exif_info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.exif_info_text.yview)
        self.exif_info_text.configure(yscrollcommand=self.exif_info_scrollbar.set)
        
        self.exif_info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.exif_info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 右半部分：选择性删除选项
        options_frame = ttk.LabelFrame(exif_frame, text="选择性删除")
        options_frame.grid(row=0, column=1, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        options_frame.columnconfigure(0, weight=1)
        options_frame.rowconfigure(1, weight=1)
        
        # 全选/取消全选按钮
        select_all_btn = ttk.Button(options_frame, text="全选", command=self._select_all_tags)
        select_all_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        deselect_all_btn = ttk.Button(options_frame, text="取消全选", command=self._deselect_all_tags)
        deselect_all_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 标签列表
        # 设置统一字体
        default_font = ('微软雅黑', 10)
        self.tags_listbox = tk.Listbox(options_frame, selectmode=tk.MULTIPLE, width=40, height=10, font=default_font)
        self.tags_scrollbar = ttk.Scrollbar(options_frame, orient=tk.VERTICAL, command=self.tags_listbox.yview)
        self.tags_listbox.configure(yscrollcommand=self.tags_scrollbar.set)
        
        self.tags_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tags_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
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
    
    def _clear_list(self):
        """清空文件列表"""
        self.selected_files.clear()
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.status_var.set("就绪")
        self.exif_info_text.delete(1.0, tk.END)
        self.tags_listbox.delete(0, tk.END)
    
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
        
        selected_tags = [self.tags_listbox.get(i) for i in self.tags_listbox.curselection()]
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
        self.tags_listbox.select_set(0, tk.END)
    
    def _deselect_all_tags(self):
        """取消全选EXIF标签"""
        self.tags_listbox.select_clear(0, tk.END)
    
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
        
        title_label = ttk.Label(title_frame, text=app_name, font=('微软雅黑', 18, 'bold'))
        title_label.pack()
        
        version_label = ttk.Label(title_frame, text=f"版本 {version}", font=('微软雅黑', 10))
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
            font=('微软雅黑', 10),
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
        author_label = ttk.Label(info_frame, text="作者:", font=('微软雅黑', 10, 'bold'))
        author_value = ttk.Label(info_frame, text="JasonShane", font=('微软雅黑', 10))
        author_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        author_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 开源协议
        license_label = ttk.Label(info_frame, text="开源协议:", font=('微软雅黑', 10, 'bold'))
        license_value = ttk.Label(info_frame, text="MIT License", font=('微软雅黑', 10))
        license_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        license_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 支持格式
        format_label = ttk.Label(info_frame, text="支持格式:", font=('微软雅黑', 10, 'bold'))
        format_value = ttk.Label(info_frame, text="JPG, JPEG, PNG, WEBP", font=('微软雅黑', 10))
        format_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        format_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 技术栈
        tech_label = ttk.Label(info_frame, text="技术栈:", font=('微软雅黑', 10, 'bold'))
        tech_value = ttk.Label(info_frame, text="Python, tkinter, piexif, Pillow", font=('微软雅黑', 10))
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
            font=('微软雅黑', 8)
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
    
    def run(self):
        """运行应用"""
        self.root.mainloop()