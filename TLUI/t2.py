import tkinter.font as font
import tkinter as tk
import time
import ctypes
import os

def install_font(font_path):
    FR_PRIVATE = 0x10
    ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("系统终端")
        # 全屏置顶设置
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        
        # 设置字体
        install_font("./System.ttf")
        self.text_font = font.Font(family="WenQuanYi Bitmap Song 12px", size=20)
        self.title_font = font.Font(family="WenQuanYi Bitmap Song 12px", size=24)
        self.rule_font = font.Font(family="WenQuanYi Bitmap Song 12px", size=18)
        self.timer_font = font.Font(family="WenQuanYi Bitmap Song 12px", size=72)
        self.button_font = font.Font(family="WenQuanYi Bitmap Song 12px", size=20)
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置行列权重
        self.main_frame.grid_columnconfigure(0, weight=1, uniform='panes')
        self.main_frame.grid_columnconfigure(1, weight=1, uniform='panes')
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # 左侧面板
        self.left_frame = tk.Frame(self.main_frame, bg='black')
        self.left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.create_left_panel()
        
        # 右侧功能区
        self.right_frame = tk.Frame(self.main_frame, bg='black')
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.create_function_panel()
        
        # 初始化倒计时（9小时）
        self.countdown_time = 9 * 60 * 60
        self.update_countdown()
        
        # 初始化输入系统
        self.user_input = ""
        self.correct_answer = "reboot"
        self.attempts = 3
        
        # 绑定ESC键退出全屏
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))

    def create_left_panel(self):
        """创建左侧面板（固定规则+题目区域）"""
        # 固定规则区域
        self.rule_frame = tk.Frame(self.left_frame, bg='black')
        self.rule_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.rules = [
            "≡≡≡ 游戏规则 ≡≡≡",
            "1. 接下来的九个小时内，你需要完成18道题目",
            "2. 每道题目只有3次机会，所以不要尝试暴力破解",
            "3. 所有傀儡电脑的文件都已被加密，虽然这对于大多数电脑都无关紧要，",
            "      但有些看起来正常的电脑其实也是傀儡电脑，想好你们将要做些什么",
            "4. 30分钟内，未完成要求题目，随机删除一台电脑的解密密钥，",
            "      理论上，你们想要解密被删除密钥的电脑需要经过几个宇宙诞生毁灭的时间了",
            "5. 9小时内，未完成所有题目，删除所有电脑的文件和EFI，",
            "      ----------，诸位尤其是老师校长都逃不了责任",
            "6. 不要尝试中断网络和关闭服务器，这只会提前启动计划，",
            "      同时会阻止你继续解题，在你看到本页面的同时，加密已经完成了。"
        ]
        
        # 创建空的规则标签用于打字机效果
        self.rule_labels = []
        for i, rule in enumerate(self.rules):
            font = self.title_font if i == 0 else self.rule_font
            label = tk.Label(
                self.rule_frame,
                text="",
                fg='red',
                bg='black',
                font=font,
                anchor='w'
            )
            label.pack(fill=tk.X, padx=20, pady=2)
            self.rule_labels.append(label)
        
        # 启动打字机效果
        self.current_rule_index = 0
        self.current_char_index = 0
        self.type_next_rule_character()
        
        # 题目区域
        self.create_question_panel()

    def type_next_rule_character(self):
        """实现规则打字机效果，5ms一个字符"""
        if self.current_rule_index < len(self.rules):
            current_rule = self.rules[self.current_rule_index]
            if self.current_char_index < len(current_rule):
                current_text = self.rule_labels[self.current_rule_index]['text']
                new_text = current_text + current_rule[self.current_char_index]
                self.rule_labels[self.current_rule_index].config(text=new_text)
                self.current_char_index += 1
                self.root.after(5, self.type_next_rule_character)
            else:
                # 当前规则完成，移动到下一条规则
                self.current_rule_index += 1
                self.current_char_index = 0
                self.root.after(5, self.type_next_rule_character)
        else:
            # 所有规则完成，开始题目打字机效果
            self.start_question_typewriter()

    def create_question_panel(self):
        """创建题目区域"""
        self.question_text = tk.Text(
            self.left_frame,
            bg='black',
            fg='red',
            font=self.text_font,
            insertbackground='red',
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            height=8
        )
        self.question_text.pack(fill=tk.BOTH, expand=True)
        self.question_text.config(state=tk.DISABLED)
        
        self.question_content = [
            "【当前验证题目】",
            "",
            "请输入系统重启指令：",
            "",
            "提示：",
            "- 该指令用于强制重启系统",
            "- 示例：reboot (正确), restart (错误)",
            "",
            "剩余尝试次数：3/3"
        ]
        
        # 初始化打字机效果变量
        self.current_question_line = 0
        self.current_question_char = 0
        self.question_lines_displayed = 0

    def start_question_typewriter(self):
        """开始题目内容的打字机效果"""
        if self.current_question_line < len(self.question_content):
            current_line = self.question_content[self.current_question_line]
            
            if self.current_question_char == 0:
                # 如果是新行，先插入换行符（除了第一行）
                if self.current_question_line > 0:
                    self.question_text.config(state=tk.NORMAL)
                    self.question_text.insert(tk.END, "\n")
                    self.question_text.config(state=tk.DISABLED)
            
            if self.current_question_char < len(current_line):
                self.question_text.config(state=tk.NORMAL)
                self.question_text.insert(tk.END, current_line[self.current_question_char])
                self.question_text.config(state=tk.DISABLED)
                self.current_question_char += 1
                self.root.after(5, self.start_question_typewriter)
            else:
                # 当前行完成，移动到下一行
                self.current_question_line += 1
                self.current_question_char = 0
                self.root.after(5, self.start_question_typewriter)
        else:
            # 所有题目内容完成
            pass

    def create_function_panel(self):
        """创建右侧功能区"""
        # 顶部区域框架（包含倒计时和输入框）
        top_frame = tk.Frame(self.right_frame, bg='black')
  
        # 1. 放大倒计时区域
        countdown_frame = tk.Frame(top_frame, bg='black')
        countdown_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.countdown_label = tk.Label(
            countdown_frame,
            text="09:00:00",
            fg='red',
            bg='black',
            font=self.timer_font
        )
        self.countdown_label.pack()
        
        # 2. 输入框区域
        input_frame = tk.Frame(top_frame, bg='black')
        input_frame.pack(fill=tk.X, pady=(0, 40))  # 增加与键盘的间距
        
        input_border = tk.Frame(input_frame, bg='red', padx=2, pady=2)
        input_border.pack()
        
        self.input_display = tk.Label(
            input_border,
            text="",
            bg='black',
            fg='red',
            font=self.text_font,
            width=30,
            height=1,
            anchor=tk.W,
            padx=10
        )
        self.input_display.pack()
        
        # 3. 键盘区域（放置在底部并居中）
        keyboard_container = tk.Frame(self.right_frame, bg='black')
        keyboard_container.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 50))  # 下移键盘
        top_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 50))
        
        # 键盘居中包装
        keyboard_center = tk.Frame(keyboard_container, bg='black')
        keyboard_center.pack()
        
        keyboard_frame = tk.Frame(keyboard_center, bg='black')
        keyboard_frame.pack()
        
        # 数字键盘行 1-9
        num_frame = tk.Frame(keyboard_frame, bg='black')
        num_frame.pack()
        
        for i in range(1, 10):
            btn = tk.Button(
                num_frame,
                text=str(i),
                bg='black',
                fg='red',
                activebackground='#330000',
                activeforeground='red',
                font=self.button_font,
                relief=tk.FLAT,
                width=3,
                command=lambda x=i: self.add_char(str(x))
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 数字0
        zero_btn = tk.Button(
            num_frame,
            text="0",
            bg='black',
            fg='red',
            activebackground='#330000',
            activeforeground='red',
            font=self.button_font,
            relief=tk.FLAT,
            width=3,
            command=lambda: self.add_char("0")
        )
        zero_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 字母键盘第一行 QWERTYUIOP
        row1_frame = tk.Frame(keyboard_frame, bg='black')
        row1_frame.pack()
        
        for char in "QWERTYUIOP":
            btn = tk.Button(
                row1_frame,
                text=char,
                bg='black',
                fg='red',
                activebackground='#330000',
                activeforeground='red',
                font=self.button_font,
                relief=tk.FLAT,
                width=3,
                command=lambda c=char: self.add_char(c)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 字母键盘第二行 ASDFGHJKL
        row2_frame = tk.Frame(keyboard_frame, bg='black')
        row2_frame.pack()
        
        for char in "ASDFGHJKL":
            btn = tk.Button(
                row2_frame,
                text=char,
                bg='black',
                fg='red',
                activebackground='#330000',
                activeforeground='red',
                font=self.button_font,
                relief=tk.FLAT,
                width=3,
                command=lambda c=char: self.add_char(c)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 字母键盘第三行 ZXCVBNM + 功能键
        row3_frame = tk.Frame(keyboard_frame, bg='black')
        row3_frame.pack()
        
        for char in "ZXCVBNM":
            btn = tk.Button(
                row3_frame,
                text=char,
                bg='black',
                fg='red',
                activebackground='#330000',
                activeforeground='red',
                font=self.button_font,
                relief=tk.FLAT,
                width=3,
                command=lambda c=char: self.add_char(c)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 功能键：清空
        clear_btn = tk.Button(
            row3_frame,
            text="清空",
            bg='black',
            fg='red',
            activebackground='#330000',
            activeforeground='red',
            font=self.button_font,
            relief=tk.FLAT,
            width=8,
            command=self.clear_input
        )
        clear_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 功能键：提交
        submit_btn = tk.Button(
            row3_frame,
            text="提交",
            bg='black',
            fg='red',
            activebackground='#330000',
            activeforeground='red',
            font=self.button_font,
            relief=tk.FLAT,
            width=8,
            command=self.check_answer
        )
        submit_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 4. 验证反馈
        feedback_frame = tk.Frame(self.right_frame, bg='black')
        feedback_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.feedback_label = tk.Label(
            feedback_frame,
            text="",
            fg='red',
            bg='black',
            font=self.text_font
        )
        self.feedback_label.pack()

    def add_char(self, char):
        """添加字符到输入框"""
        if len(self.user_input) < 10:
            self.user_input += char
            self.input_display.config(text=self.user_input)
            self.feedback_label.config(text="")

    def clear_input(self):
        """清空输入框"""
        self.user_input = ""
        self.input_display.config(text="")
        self.feedback_label.config(text="")

    def check_answer(self):
        """验证答案"""
        if not self.user_input:
            return
            
        if self.user_input.lower() == self.correct_answer:
            self.feedback_label.config(text="验证通过！", fg='#00FF00')
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete(1.0, tk.END)
            self.question_text.insert(tk.END, "验证成功！系统即将重启...")
            self.question_text.config(state=tk.DISABLED)
            os._exit(0)
        else:
            self.attempts -= 1
            if self.attempts > 0:
                self.feedback_label.config(
                    text=f"验证失败！剩余尝试次数：{self.attempts}/3", 
                    fg='red'
                )
                self.question_text.config(state=tk.NORMAL)
                content = self.question_text.get(1.0, tk.END).split("\n")
                content[-1] = f"剩余尝试次数：{self.attempts}/3"
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(tk.END, "\n".join(content))
                self.question_text.config(state=tk.DISABLED)
            else:
                self.feedback_label.config(text="验证失败！系统已锁定", fg='red')
                self.input_display.config(text="******")
                self.question_text.config(state=tk.NORMAL)
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(tk.END, "系统已永久锁定！\n\n请联系管理员")
                self.question_text.config(state=tk.DISABLED)
        
        if self.user_input.lower() == self.correct_answer or self.attempts <= 0:
            self.root.after(3000, lambda: self.feedback_label.config(text=""))
        self.user_input = ""

    def update_countdown(self):
        """更新倒计时显示"""
        if self.countdown_time > 0:
            hours = self.countdown_time // 3600
            minutes = (self.countdown_time % 3600) // 60
            seconds = self.countdown_time % 60
            self.countdown_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.countdown_time -= 1
            self.root.after(1000, self.update_countdown)
        else:
            self.countdown_label.config(text="时间到！")
            if self.user_input.lower() != self.correct_answer:
                self.feedback_label.config(text="时间到！系统已锁定", fg='red')
                self.input_display.config(text="******")
                self.question_text.config(state=tk.NORMAL)
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(tk.END, "系统已永久锁定！\n\n请联系管理员")
                self.question_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()