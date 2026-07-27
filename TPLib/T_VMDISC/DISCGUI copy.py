import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import zipfile
import os
import shutil
import tempfile
import subprocess
import platform
from tkinterdnd2 import *
from datetime import datetime
import hashlib
import time
import json

class ZipManager:
    def __init__(self, root):
        self.root = root
        self.root.title("ZIP文件管理器")
        self.root.geometry("1200x600")
        
        # 当前打开的ZIP文件
        self.current_zip = None
        self.current_path = []  # 当前在ZIP中的路径
        self.selected_items = []
        self.clipboard_items = []  # 用于复制/粘贴操作的剪贴板
        self.clipboard_operation = None  # 'copy' 或 'move'
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建导航栏
        self.create_navigation()
        
        # 创建文件列表
        self.create_file_list()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 绑定拖拽事件
        self.setup_drag_drop()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建压缩包", command=self.new_archive)
        file_menu.add_command(label="打开压缩包", command=self.open_archive)
        file_menu.add_separator()
        file_menu.add_command(label="重命名", command=self.rename_selected)
        file_menu.add_command(label="删除", command=self.delete_selected)
        file_menu.add_separator()
        file_menu.add_command(label="解压到", command=self.extract_to)
        file_menu.add_command(label="CRC校验", command=self.check_crc)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="全选", command=self.select_all)
        edit_menu.add_command(label="全部取消", command=self.deselect_all)
        edit_menu.add_command(label="反选", command=self.invert_selection)
        edit_menu.add_separator()
        edit_menu.add_command(label="选择（掩码）", command=self.select_by_mask)
        edit_menu.add_command(label="取消选择（掩码）", command=self.deselect_by_mask)
        edit_menu.add_separator()
        edit_menu.add_command(label="复制", command=self.copy_selected)
        edit_menu.add_command(label="粘贴", command=self.paste_items)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="基准测试", command=self.benchmark)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
        
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # 工具栏按钮
        ttk.Button(toolbar, text="添加", command=self.add_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="解压", command=self.extract_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="测试", command=self.test_archive).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="复制", command=self.copy_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="移动", command=self.move_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="删除", command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="信息", command=self.show_info).pack(side=tk.LEFT, padx=2)
        
    def create_navigation(self):
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # 返回上层按钮
        ttk.Button(nav_frame, text="↑", width=3, command=self.go_up).pack(side=tk.LEFT, padx=2)
        
        # 路径显示
        self.path_label = ttk.Label(nav_frame, text="", anchor=tk.W)
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
    def create_file_list(self):
        # 创建一个主Frame来容纳Treeview和滚动条
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建Treeview
        columns = ('名称', '大小', '类型', '修改时间')
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='tree headings')
        
        # 设置列
        self.tree.heading('#0', text='')
        self.tree.heading('名称', text='名称')
        self.tree.heading('大小', text='大小')
        self.tree.heading('类型', text='类型')
        self.tree.heading('修改时间', text='修改时间')
        
        # 设置列宽
        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('名称', width=200)
        self.tree.column('大小', width=100)
        self.tree.column('类型', width=100)
        self.tree.column('修改时间', width=150)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局Treeview和滚动条
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定事件
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.on_right_click)
        
        # 创建右键菜单
        self.create_context_menu()
        
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="重命名", command=self.rename_selected)
        self.context_menu.add_command(label="删除", command=self.delete_selected)
        self.context_menu.add_command(label="查看属性", command=self.show_properties)
        self.context_menu.add_command(label="创建链接", command=self.create_link)
        self.context_menu.add_command(label="CRC校验", command=self.check_crc)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="复制", command=self.copy_selected)
        self.context_menu.add_command(label="移动", command=self.move_selected)
        
        # 空白区域右键菜单
        self.empty_context_menu = tk.Menu(self.root, tearoff=0)
        self.empty_context_menu.add_command(label="新建文件", command=self.new_file)
        self.empty_context_menu.add_command(label="新建文件夹", command=self.new_folder)
        self.empty_context_menu.add_separator()
        if self.clipboard_items and self.clipboard_operation:
            self.empty_context_menu.add_command(label="粘贴", command=self.paste_items)
        
    def create_status_bar(self):
        # 状态栏单独放在窗口底部
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_drag_drop(self):
        # 注册拖放目标
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self.on_drop)
        
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.add_files_to_archive(files)
        
    def new_archive(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if filename:
            try:
                # 使用最高压缩等级创建ZIP文件
                with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                    pass
                self.current_zip = filename
                self.current_path = []
                self.update_file_list()
                self.update_status(f"新建压缩包: {filename} (最高压缩等级)")
            except Exception as e:
                messagebox.showerror("错误", f"创建压缩包失败: {str(e)}")
                
    def open_archive(self):
        filename = filedialog.askopenfilename(
            filetypes=[("ZIP文件", "*.zip"), ("所有文件", "*.*")]
        )
        if filename:
            try:
                with zipfile.ZipFile(filename, 'r') as zf:
                    # 测试文件是否有效
                    zf.testzip()
                self.current_zip = filename
                self.current_path = []
                self.update_file_list()
                self.update_status(f"打开压缩包: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"打开压缩包失败: {str(e)}")
                
    def update_file_list(self):
        # 清空列表
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not self.current_zip:
            return
            
        try:
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                # 添加返回上层按钮
                if self.current_path:
                    self.tree.insert('', 'end', values=('..', '', '文件夹', ''), tags=('folder',))
                
                # 获取当前路径的文件和文件夹
                current_path_str = '/'.join(self.current_path) + '/' if self.current_path else ''
                
                folders = set()
                files = []
                
                for info in zf.infolist():
                    filename = info.filename
                    if filename.startswith(current_path_str):
                        relative_path = filename[len(current_path_str):]
                        if '/' in relative_path:
                            # 这是一个文件夹
                            folder_name = relative_path.split('/')[0]
                            folders.add(folder_name)
                        else:
                            # 这是一个文件
                            files.append((relative_path, info))
                
                # 添加文件夹
                for folder in sorted(folders):
                    self.tree.insert('', 'end', values=(folder, '', '文件夹', ''), tags=('folder',))
                
                # 添加文件
                for filename, info in sorted(files):
                    size = self.format_size(info.file_size)
                    date = datetime(*info.date_time).strftime('%Y-%m-%d %H:%M:%S')
                    file_type = self.get_file_type(filename)
                    self.tree.insert('', 'end', values=(filename, size, file_type, date), tags=('file',))
                    
        except Exception as e:
            messagebox.showerror("错误", f"读取文件列表失败: {str(e)}")
            
        # 更新路径显示
        path_str = '/'.join(self.current_path)
        self.path_label.config(text=path_str if path_str else '根目录')
        
        # 更新右键菜单，显示或隐藏粘贴选项
        self.create_context_menu()
        
    def get_file_type(self, filename):
        """根据文件扩展名返回文件类型描述"""
        _, ext = os.path.splitext(filename.lower())
        file_types = {
            '.txt': '文本文档',
            '.doc': 'Word文档',
            '.docx': 'Word文档',
            '.xls': 'Excel表格',
            '.xlsx': 'Excel表格',
            '.ppt': 'PowerPoint',
            '.pptx': 'PowerPoint',
            '.pdf': 'PDF文档',
            '.jpg': 'JPEG图像',
            '.jpeg': 'JPEG图像',
            '.png': 'PNG图像',
            '.gif': 'GIF图像',
            '.bmp': '位图',
            '.mp3': 'MP3音频',
            '.wav': 'WAV音频',
            '.mp4': 'MP4视频',
            '.avi': 'AVI视频',
            '.mkv': 'MKV视频',
            '.zip': 'ZIP压缩包',
            '.rar': 'RAR压缩包',
            '.7z': '7-Zip压缩包',
            '.exe': '应用程序',
            '.dll': '动态链接库',
            '.py': 'Python脚本',
            '.js': 'JavaScript文件',
            '.html': 'HTML文档',
            '.css': '样式表',
            '.json': 'JSON数据',
            '.xml': 'XML文档',
        }
        return file_types.get(ext, f'{ext}文件')
        
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
        
    def on_double_click(self, event):
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        name = item['values'][0]
        
        if name == '..':
            self.go_up()
        elif item['tags'] and 'folder' in item['tags']:
            # 进入文件夹
            self.current_path.append(str(name))
            self.update_file_list()
        else:
            # 打开文件
            self.open_file(name)
            
    def go_up(self):
        if self.current_path:
            self.current_path.pop()
            self.update_file_list()
            
    def open_file(self, filename):
        if not self.current_zip:
            return
            
        try:
            # 创建临时文件
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, str(filename))
            
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                file_path = '/'.join(self.current_path + [str(filename)])
                with open(temp_file, 'wb') as f:
                    f.write(zf.read(file_path))
            
            # 用系统默认程序打开
            if platform.system() == 'Windows':
                os.startfile(temp_file)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', temp_file])
            else:
                subprocess.run(['xdg-open', temp_file])
                
        except Exception as e:
            messagebox.showerror("错误", f"打开文件失败: {str(e)}")
            
    def on_right_click(self, event):
        # 获取点击位置的项目
        item = self.tree.identify('item', event.x, event.y)
        
        if item:
            # 右键点击文件/文件夹
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
        else:
            # 右键点击空白区域
            self.empty_context_menu.post(event.x_root, event.y_root)
            
    def add_files(self):
        if not self.current_zip:
            messagebox.showwarning("警告", "请先打开或创建一个压缩包")
            return
            
        filenames = filedialog.askopenfilenames()
        if filenames:
            self.add_files_to_archive(filenames)
            
    def add_files_to_archive(self, filenames):
        if not self.current_zip:
            return
            
        try:
            # 使用最高压缩等级添加文件
            with zipfile.ZipFile(self.current_zip, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for filename in filenames:
                    if os.path.isdir(filename):
                        # 添加文件夹及其内容
                        self.add_folder_to_zip(zf, filename, '')
                    else:
                        # 添加单个文件
                        arcname = '/'.join(self.current_path + [os.path.basename(filename)])
                        zf.write(filename, arcname)
                        
            self.update_file_list()
            self.update_status(f"已添加 {len(filenames)} 个文件 (最高压缩等级)")
            
        except Exception as e:
            messagebox.showerror("错误", f"添加文件失败: {str(e)}")
            
    def add_folder_to_zip(self, zf, folder_path, arcpath):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(str(root), str(file))
                rel_path = os.path.relpath(file_path, folder_path)
                arcname = '/'.join(self.current_path + [str(arcpath), str(rel_path)])
                zf.write(file_path, arcname)
                
    def extract_selected(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if not selection:
            return
            
        folder = filedialog.askdirectory()
        if not folder:
            return
            
        try:
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                for item in selection:
                    values = self.tree.item(item)['values']
                    name = values[0]
                    
                    if name == '..':
                        continue
                        
                    if 'folder' in self.tree.item(item)['tags']:
                        # 提取文件夹
                        folder_path = '/'.join(self.current_path + [str(name)])
                        for info in zf.infolist():
                            if info.filename.startswith(folder_path + '/'):
                                zf.extract(info, folder)
                    else:
                        # 提取文件
                        file_path = '/'.join(self.current_path + [str(name)])
                        zf.extract(file_path, folder)
                        
            self.update_status(f"已提取 {len(selection)} 个项目")
            
        except Exception as e:
            messagebox.showerror("错误", f"提取失败: {str(e)}")
            
    def extract_to(self):
        self.extract_selected()
        
    def delete_selected(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if not selection:
            return
            
        if not messagebox.askyesno("确认", "确定要删除选中的项目吗？"):
            return
            
        try:
            # 创建临时文件
            temp_dir = tempfile.mkdtemp()
            temp_zip = os.path.join(temp_dir, 'temp.zip')
            
            with zipfile.ZipFile(self.current_zip, 'r') as zf_in:
                # 使用最高压缩等级创建临时ZIP
                with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf_out:
                    # 复制不需要删除的文件
                    for info in zf_in.infolist():
                        should_delete = False
                        
                        for item in selection:
                            values = self.tree.item(item)['values']
                            name = values[0]
                            
                            if name == '..':
                                continue
                                
                            if 'folder' in self.tree.item(item)['tags']:
                                # 检查是否在要删除的文件夹中
                                folder_path = '/'.join(self.current_path + [str(name)])
                                if info.filename.startswith(folder_path + '/'):
                                    should_delete = True
                                    break
                            else:
                                # 检查是否是要删除的文件
                                file_path = '/'.join(self.current_path + [str(name)])
                                if info.filename == file_path:
                                    should_delete = True
                                    break
                                    
                        if not should_delete:
                            zf_out.writestr(info, zf_in.read(info.filename))
                            
            # 替换原文件
            shutil.move(temp_zip, self.current_zip)
            shutil.rmtree(temp_dir)
            
            self.update_file_list()
            self.update_status(f"已删除 {len(selection)} 个项目")
            
        except Exception as e:
            messagebox.showerror("错误", f"删除失败: {str(e)}")
            
    def rename_selected(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if len(selection) != 1:
            messagebox.showwarning("警告", "请选择一个项目进行重命名")
            return
            
        item = selection[0]
        values = self.tree.item(item)['values']
        old_name = values[0]
        
        if old_name == '..':
            return
            
        new_name = simpledialog.askstring("重命名", "请输入新名称:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
            
        try:
            # 创建临时文件
            temp_dir = tempfile.mkdtemp()
            temp_zip = os.path.join(temp_dir, 'temp.zip')
            
            with zipfile.ZipFile(self.current_zip, 'r') as zf_in:
                # 使用最高压缩等级创建临时ZIP
                with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf_out:
                    for info in zf_in.infolist():
                        if 'folder' in self.tree.item(item)['tags']:
                            # 重命名文件夹
                            old_path = '/'.join(self.current_path + [str(old_name)])
                            new_path = '/'.join(self.current_path + [str(new_name)])
                            
                            if info.filename.startswith(old_path + '/'):
                                new_filename = info.filename.replace(old_path + '/', new_path + '/')
                                zf_out.writestr(new_filename, zf_in.read(info.filename))
                            else:
                                zf_out.writestr(info, zf_in.read(info.filename))
                        else:
                            # 重命名文件
                            old_path = '/'.join(self.current_path + [str(old_name)])
                            new_path = '/'.join(self.current_path + [str(new_name)])
                            
                            if info.filename == old_path:
                                zf_out.writestr(new_path, zf_in.read(info.filename))
                            else:
                                zf_out.writestr(info, zf_in.read(info.filename))
                                
            # 替换原文件
            shutil.move(temp_zip, self.current_zip)
            shutil.rmtree(temp_dir)
            
            self.update_file_list()
            self.update_status(f"已重命名: {old_name} -> {new_name}")
            
        except Exception as e:
            messagebox.showerror("错误", f"重命名失败: {str(e)}")
            
    def select_all(self):
        for item in self.tree.get_children():
            self.tree.selection_add(item)
            
    def deselect_all(self):
        for item in self.tree.get_children():
            self.tree.selection_remove(item)
            
    def invert_selection(self):
        for item in self.tree.get_children():
            if item in self.tree.selection():
                self.tree.selection_remove(item)
            else:
                self.tree.selection_add(item)
                
    def select_by_mask(self):
        mask = simpledialog.askstring("选择", "请输入选择掩码 (例如: *.txt):")
        if mask:
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                name = values[0]
                if self.match_mask(name, mask):
                    self.tree.selection_add(item)
                    
    def deselect_by_mask(self):
        mask = simpledialog.askstring("取消选择", "请输入取消选择掩码 (例如: *.txt):")
        if mask:
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                name = values[0]
                if self.match_mask(name, mask):
                    self.tree.selection_remove(item)
                    
    def match_mask(self, name, mask):
        import fnmatch
        return fnmatch.fnmatch(name, mask)
        
    def test_archive(self):
        if not self.current_zip:
            messagebox.showwarning("警告", "请先打开一个压缩包")
            return
            
        try:
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                bad_file = zf.testzip()
                if bad_file:
                    messagebox.showerror("测试结果", f"发现损坏的文件: {bad_file}")
                else:
                    messagebox.showinfo("测试结果", "压缩包测试通过，没有发现损坏的文件")
                    
        except Exception as e:
            messagebox.showerror("错误", f"测试失败: {str(e)}")
            
    def check_crc(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if not selection:
            return
            
        try:
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                results = []
                for item in selection:
                    values = self.tree.item(item)['values']
                    name = values[0]
                    
                    if name == '..' or 'folder' in self.tree.item(item)['tags']:
                        continue
                        
                    file_path = '/'.join(self.current_path + [str(name)])
                    data = zf.read(file_path)
                    crc = hashlib.crc32(data) & 0xffffffff
                    results.append(f"{name}: CRC32 = {crc:08X}")
                    
                if results:
                    messagebox.showinfo("CRC校验结果", '\n'.join(results))
                    
        except Exception as e:
            messagebox.showerror("错误", f"CRC校验失败: {str(e)}")
            
    def show_properties(self):
        selection = self.tree.selection()
        if not selection:
            return
            
        item = selection[0]
        values = self.tree.item(item)['values']
        name = values[0]
        
        if name == '..':
            return
            
        try:
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                if 'folder' in self.tree.item(item)['tags']:
                    # 文件夹属性
                    folder_path = '/'.join(self.current_path + [str(name)])
                    file_count = 0
                    total_size = 0
                    compressed_size = 0
                    
                    for info in zf.infolist():
                        if info.filename.startswith(folder_path + '/'):
                            file_count += 1
                            total_size += info.file_size
                            compressed_size += info.compress_size
                            
                    props = f"名称: {name}\n"
                    props += f"类型: 文件夹\n"
                    props += f"文件数: {file_count}\n"
                    props += f"总大小: {self.format_size(total_size)}\n"
                    props += f"压缩后大小: {self.format_size(compressed_size)}\n"
                    if total_size > 0:
                        props += f"压缩率: {(1 - compressed_size/total_size)*100:.1f}%"
                else:
                    # 文件属性
                    file_path = '/'.join(self.current_path + [str(name)])
                    info = zf.getinfo(file_path)
                    
                    props = f"名称: {name}\n"
                    props += f"类型: 文件\n"
                    props += f"大小: {self.format_size(info.file_size)}\n"
                    props += f"压缩后: {self.format_size(info.compress_size)}\n"
                    props += f"压缩率: {(1 - info.compress_size/info.file_size)*100:.1f}%\n"
                    props += f"修改时间: {datetime(*info.date_time).strftime('%Y-%m-%d %H:%M:%S')}\n"
                    props += f"CRC32: {info.CRC:08X}\n"
                    props += f"压缩方法: {info.compress_type}"
                    
                messagebox.showinfo("属性", props)
                
        except Exception as e:
            messagebox.showerror("错误", f"获取属性失败: {str(e)}")
            
    def create_link(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要创建链接的文件")
            return
            
        item = selection[0]
        values = self.tree.item(item)['values']
        name = values[0]
        
        if name == '..' or 'folder' in self.tree.item(item)['tags']:
            messagebox.showwarning("警告", "只能为文件创建链接")
            return
            
        link_name = simpledialog.askstring("创建链接", "请输入链接名称:", initialvalue=f"链接到_{name}")
        if not link_name:
            return
            
        try:
            # 创建链接信息
            file_path = '/'.join(self.current_path + [str(name)])
            link_info = {
                "type": "link",
                "target": file_path,
                "created": datetime.now().isoformat()
            }
            
            # 创建临时文件
            temp_dir = tempfile.mkdtemp()
            temp_zip = os.path.join(temp_dir, 'temp.zip')
            
            with zipfile.ZipFile(self.current_zip, 'r') as zf_in:
                # 使用最高压缩等级创建临时ZIP
                with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf_out:
                    # 复制所有文件
                    for info in zf_in.infolist():
                        zf_out.writestr(info, zf_in.read(info.filename))
                    
                    # 添加链接文件
                    link_path = '/'.join(self.current_path + [str(link_name)])
                    zf_out.writestr(link_path, json.dumps(link_info))
                    
            # 替换原文件
            shutil.move(temp_zip, self.current_zip)
            shutil.rmtree(temp_dir)
            
            self.update_file_list()
            self.update_status(f"已创建链接: {link_name}")
            
        except Exception as e:
            messagebox.showerror("错误", f"创建链接失败: {str(e)}")
            
    def new_file(self):
        if not self.current_zip:
            return
            
        filename = simpledialog.askstring("新建文件", "请输入文件名:")
        if filename:
            try:
                # 使用最高压缩等级
                with zipfile.ZipFile(self.current_zip, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                    file_path = '/'.join(self.current_path + [str(filename)])
                    zf.writestr(file_path, '')
                    
                self.update_file_list()
                self.update_status(f"已创建文件: {filename}")
                
            except Exception as e:
                messagebox.showerror("错误", f"创建文件失败: {str(e)}")
                
    def new_folder(self):
        if not self.current_zip:
            return
            
        foldername = simpledialog.askstring("新建文件夹", "请输入文件夹名:")
        if foldername:
            try:
                # 使用最高压缩等级
                with zipfile.ZipFile(self.current_zip, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                    folder_path = '/'.join(self.current_path + [str(foldername)]) + '/'
                    zf.writestr(folder_path, '')
                    
                self.update_file_list()
                self.update_status(f"已创建文件夹: {foldername}")
                
            except Exception as e:
                messagebox.showerror("错误", f"创建文件夹失败: {str(e)}")
                
    def copy_selected(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if not selection:
            return
            
        # 保存选中的项目到剪贴板
        self.clipboard_items = []
        self.clipboard_operation = 'copy'
        
        for item in selection:
            values = self.tree.item(item)['values']
            name = values[0]
            
            if name == '..':
                continue
                
            is_folder = 'folder' in self.tree.item(item)['tags']
            self.clipboard_items.append({
                'name': name,
                'is_folder': is_folder,
                'path': '/'.join(self.current_path + [str(name)])
            })
            
        self.update_status(f"已复制 {len(self.clipboard_items)} 个项目")
        # 更新右键菜单，显示粘贴选项
        self.create_context_menu()
        
    def move_selected(self):
        if not self.current_zip:
            return
            
        selection = self.tree.selection()
        if not selection:
            return
            
        # 保存选中的项目到剪贴板
        self.clipboard_items = []
        self.clipboard_operation = 'move'
        
        for item in selection:
            values = self.tree.item(item)['values']
            name = values[0]
            
            if name == '..':
                continue
                
            is_folder = 'folder' in self.tree.item(item)['tags']
            self.clipboard_items.append({
                'name': name,
                'is_folder': is_folder,
                'path': '/'.join(self.current_path + [str(name)])
            })
            
        self.update_status(f"已移动 {len(self.clipboard_items)} 个项目")
        # 更新右键菜单，显示粘贴选项
        self.create_context_menu()
        
    def paste_items(self):
        if not self.current_zip or not self.clipboard_items:
            return
            
        try:
            # 创建临时文件
            temp_dir = tempfile.mkdtemp()
            temp_zip = os.path.join(temp_dir, 'temp.zip')
            
            with zipfile.ZipFile(self.current_zip, 'r') as zf_in:
                # 使用最高压缩等级创建临时ZIP
                with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf_out:
                    # 复制所有文件，除了要移动的文件
                    for info in zf_in.infolist():
                        should_skip = False
                        
                        if self.clipboard_operation == 'move':
                            for item in self.clipboard_items:
                                if item['is_folder']:
                                    # 检查是否在要移动的文件夹中
                                    if info.filename.startswith(item['path'] + '/'):
                                        should_skip = True
                                        break
                                else:
                                    # 检查是否是要移动的文件
                                    if info.filename == item['path']:
                                        should_skip = True
                                        break
                        
                        if not should_skip:
                            zf_out.writestr(info, zf_in.read(info.filename))
                    
                    # 粘贴剪贴板中的项目
                    for item in self.clipboard_items:
                        new_path = '/'.join(self.current_path + [item['name']])
                        
                        if item['is_folder']:
                            # 粘贴文件夹
                            folder_path = item['path']
                            
                            # 创建文件夹标记
                            zf_out.writestr(new_path + '/', '')
                            
                            # 复制文件夹内容
                            for info in zf_in.infolist():
                                if info.filename.startswith(folder_path + '/'):
                                    # 计算新的路径
                                    rel_path = info.filename[len(folder_path)+1:]
                                    new_file_path = new_path + '/' + rel_path
                                    zf_out.writestr(new_file_path, zf_in.read(info.filename))
                        else:
                            # 粘贴文件
                            zf_out.writestr(new_path, zf_in.read(item['path']))
                    
            # 替换原文件
            shutil.move(temp_zip, self.current_zip)
            shutil.rmtree(temp_dir)
            
            # 如果是移动操作，清空剪贴板
            if self.clipboard_operation == 'move':
                self.clipboard_items = []
                self.clipboard_operation = None
            
            self.update_file_list()
            self.update_status(f"已粘贴 {len(self.clipboard_items)} 个项目")
            
            # 更新右键菜单
            self.create_context_menu()
            
        except Exception as e:
            messagebox.showerror("错误", f"粘贴失败: {str(e)}")
            
    def show_info(self):
        if not self.current_zip:
            messagebox.showwarning("警告", "请先打开一个压缩包")
            return
            
        try:
            with zipfile.ZipFile(self.current_zip, 'r') as zf:
                file_count = 0
                folder_count = 0
                total_size = 0
                compressed_size = 0
                
                for info in zf.infolist():
                    if info.filename.endswith('/'):
                        folder_count += 1
                    else:
                        file_count += 1
                        total_size += info.file_size
                        compressed_size += info.compress_size
                        
                info_text = f"文件名: {os.path.basename(self.current_zip)}\n"
                info_text += f"路径: {os.path.dirname(self.current_zip)}\n"
                info_text += f"文件夹数: {folder_count}\n"
                info_text += f"文件数: {file_count}\n"
                info_text += f"原始大小: {self.format_size(total_size)}\n"
                info_text += f"压缩后大小: {self.format_size(compressed_size)}\n"
                if total_size > 0:
                    info_text += f"压缩率: {(1 - compressed_size/total_size)*100:.1f}%"
                
                messagebox.showinfo("压缩包信息", info_text)
                
        except Exception as e:
            messagebox.showerror("错误", f"获取信息失败: {str(e)}")
            
    def benchmark(self):
        if not self.current_zip:
            messagebox.showwarning("警告", "请先打开一个压缩包")
            return
            
        try:
            # 创建临时文件用于测试
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, 'benchmark_test.txt')
            
            # 创建测试文件
            with open(temp_file, 'w') as f:
                f.write('A' * 1000000)  # 1MB测试文件
                
            # 测试压缩速度
            start_time = time.time()
            temp_zip = os.path.join(temp_dir, 'benchmark_test.zip')
            with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                zf.write(temp_file, 'test.txt')
            compress_time = time.time() - start_time
            
            # 测试解压速度
            start_time = time.time()
            with zipfile.ZipFile(temp_zip, 'r') as zf:
                zf.extract('test.txt', temp_dir)
            extract_time = time.time() - start_time
            
            # 获取文件大小
            original_size = os.path.getsize(temp_file)
            compressed_size = os.path.getsize(temp_zip)
            
            # 计算速度
            compress_speed = original_size / (1024 * 1024) / compress_time  # MB/s
            extract_speed = original_size / (1024 * 1024) / extract_time  # MB/s
            
            # 显示结果
            result = f"基准测试结果:\n\n"
            result += f"原始大小: {self.format_size(original_size)}\n"
            result += f"压缩后大小: {self.format_size(compressed_size)}\n"
            result += f"压缩率: {(1 - compressed_size/original_size)*100:.1f}%\n\n"
            result += f"压缩速度: {compress_speed:.2f} MB/s\n"
            result += f"解压速度: {extract_speed:.2f} MB/s"
            
            messagebox.showinfo("基准测试结果", result)
            
            # 清理临时文件
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            messagebox.showerror("错误", f"基准测试失败: {str(e)}")
            
    def show_about(self):
        about_text = "ZIP文件管理器 v1.0\n\n"
        about_text += "一个仿照7-ZIP的ZIP文件管理器\n"
        about_text += "使用Python tkinter开发\n\n"
        about_text += "功能包括:\n"
        about_text += "- 创建和打开ZIP文件\n"
        about_text += "- 添加、删除、重命名文件\n"
        about_text += "- 文件夹浏览\n"
        about_text += "- 拖拽添加文件\n"
        about_text += "- CRC校验\n"
        about_text += "- 文件属性查看\n"
        about_text += "- 文件复制和移动\n"
        about_text += "- 创建链接\n"
        about_text += "- 基准测试"
        
        messagebox.showinfo("关于", about_text)
        
    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ZipManager(root)
    root.mainloop()