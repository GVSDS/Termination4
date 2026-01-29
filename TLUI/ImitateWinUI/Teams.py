import tkinter as tk
import time


class Teams(tk.Tk):
    def __init__(self):
        super().__init__()
        self.OverBackGround = "#1d1f1e"
        self.BackGround = "#004277"
        # self.TipWindow.attributes("-topmost", True)
        self.state("zoomed")
        self.title("Microsoft Teams")
        self.configure(bg="#000")

        self.Agreement = tk.Frame(self, bg=self.BackGround)
        self.Agreement.pack(padx=300, pady=100, fill="both", expand=True)

        # self.Nav = tk.Frame(self.Agreement, bg=self.OverBackGround, height=60)
        # self.Nav.pack(fill="x", side="top")

        self.Body = tk.Frame(self.Agreement, bg=self.BackGround, width=100)
        self.Body.pack(fill="both", expand=True)

        tk.Label(self.Body, text="同意个人数据跨境传输", bg=self.BackGround, fg="#fff", font=("华文细黑", 30)).pack(pady=50)
        tk.Label(
            self.Body,
            text="""当您在使用本产品以及列在"了解更多"页面中的产品和服务（统称"产品”）时，微软会将一些对于向您提供和运行产品所必要的个人数据传输至中国大
陆之外。如果您选择传输，一些产品允许您发送额外的可选数据至中国大陆之外。传输的数据将被加密，除非您采取主动操作进行跨境传输，如主动
将数据存储于境外云服务提供商，否则存储在您本地设备上的数据不会被传输出去。

如果您不同意传输对于提供本产品或者列在"了解更多"页面中的产品所必要的数据，您可以选择停止使用该产品。您可以在产品的使用条款中了解是
否能获得退款。欲了解关于向微软商店退还产品的信息，请访问https://aka.ms/refund。

https://aka.ms/refund

微软会根据Microsoft隐私声明处理以及传输数据，欲解更多关于数据跨境传输的信息和如何联系我们，请访问“了解更多”页面

https://aka.ms/privacy""",
            font=("华文细黑", 13),
            bg=self.BackGround,
            fg="white",
            anchor="w",
            justify="left"
        ).pack(pady=0, padx=50, fill="x")
        self.update()

        self.Footer = tk.Frame(self.Agreement, bg=self.OverBackGround, height=60)
        self.Footer.pack(fill="x", side="bottom")

        self.bind("<Button-3>", self.CloseAll)
    
    def CloseAll(self, event):
        self.destroy()


if __name__ == "__main__":
    _ = Teams()
    _.mainloop()