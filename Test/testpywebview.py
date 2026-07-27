import tkinter as tk
from tkinter import ttk
import webview
import threading

class WebViewApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tkinter + PyWebView")
        self.root.geometry("800x600")
        
        # 创建容器Frame
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # 在单独线程中启动WebView
        self.start_webview()
        
        self.root.mainloop()
    
    def start_webview(self):
        def create_webview():
            window_handle = self.container.winfo_id()
            webview.create_window(
                "Embedded Browser",
                url="https://www.example.com",
                width=800,
                height=600,
                parent=window_handle
            )
            webview.start()
            
        thread = threading.Thread(target=create_webview)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    app = WebViewApp()