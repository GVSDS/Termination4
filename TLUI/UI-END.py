import tkinter as tk
from PIL import Image, ImageTk


class CreditsScroller:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        self.root.title("THE END")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.credits_frame = tk.Frame(self.canvas, bg="black", width=1000)


        tk.Label(self.credits_frame, text="COMPANY", fg="white", bg="black", font=("微软雅黑", 20)).pack()
        self.F1 = self.add_column(width=800, height=170)
        self.I1 = Image.open("./THEND/GVSDS.jpg").resize((300, 120))
        self.P1 = ImageTk.PhotoImage(self.I1)
        tk.Label(self.F1, image=self.P1, bg="black").pack(side=tk.LEFT)
        tk.Label(self.F1, text="\nGreen Valley Secure\nData Solutions", fg="white", bg="black", font=("微软雅黑", 15)).pack(side=tk.RIGHT)

        self.add_space(50)

        tk.Label(self.credits_frame, text="DEVELOPERS", fg="white", bg="black", font=("微软雅黑", 20)).pack()
        self.F2 = self.add_column(width=800, height=170)
        self.I2 = Image.open("./THEND/Veyra.png").resize((250, 170))
        self.P2 = ImageTk.PhotoImage(self.I2)
        tk.Label(self.F2, image=self.P2, bg="black").pack(side=tk.LEFT)
        tk.Label(self.F2, text="Veyra", fg="white", bg="black", font=("微软雅黑", 15)).pack(side=tk.RIGHT)

        self.F_3 = self.add_column(width=800, height=170)
        tk.Label(self.F_3, text=":(", bg="black", font=("微软雅黑", 40)).pack(side=tk.LEFT)
        tk.Label(self.F_3, text="YRZD", fg="white", bg="black", font=("微软雅黑", 15)).pack(side=tk.RIGHT)

        self.add_space(50)

        tk.Label(self.credits_frame, text="LANGUAGE", fg="white", bg="black", font=("微软雅黑", 20)).pack()
        self.F3 = self.add_column(width=800, height=15, topspace=10)
        tk.Label(self.F3, text=" [NAME]", fg="white", bg="black", font=("微软雅黑", 15)).pack(side=tk.LEFT)
        tk.Label(self.F3, text="[VERSION] ", fg="white", bg="black", font=("微软雅黑", 15)).pack(side=tk.RIGHT)

        self.F4 = self.add_column(width=800, height=15)
        tk.Label(self.F4, text="Python", fg="white", bg="black", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        tk.Label(self.F4, text="3.12.0 64-bit ('.ENV': venv) (Win32 64-bit Core)", fg="white", bg="black", font=("微软雅黑", 10)).pack(side=tk.RIGHT)

        self.F5 = self.add_column(width=800, height=15)
        tk.Label(self.F5, text="C", fg="white", bg="black", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        tk.Label(self.F5, text="MinGW-W64-builds-4.3.5", fg="white", bg="black", font=("微软雅黑", 10)).pack(side=tk.RIGHT)

        self.F6 = self.add_column(width=800, height=15)
        tk.Label(self.F6, text="C++", fg="white", bg="black", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        tk.Label(self.F6, text="MinGW-W64-builds-4.3.5", fg="white", bg="black", font=("微软雅黑", 10)).pack(side=tk.RIGHT)

        self.add_space(50)

        tk.Label(self.credits_frame, text="T4.1.0 Final Chapter - \"Things\"", fg="white", bg="black", font=("微软雅黑", 20)).pack()
        ENDTEXT=r"""I deeply feel that what I did was wrong

My purpose for creating this virus itself may be to show off my skills,
although I don't have any skills to show off now.
Another purpose is to tell others and me:
    1. I am still so excellent,
    2. I am still not inferior to others, and
    3. I still have the capital to compare myself with classmates and even teachers.
    4. I am not Brother B,
    5. I am not just a waiter who appears at the odd jobs scene.
    6. I should be the protagonist of my own life,
and this world was born for me.
This virus has iterated five times, namely O1 W2、O3、T4、T4.1, Among them,
T4.1 is the PLUS iteration version of T4, which is the best I can do
in a short period of time and extremely complex psychological environment.
Although I write every day, I actually haven't written much.
I have about 4-5 years of programming experience now,
    but I can't find a decent project on my computer.
I have been tormented by myself because of some experiences when I was a child.
    In middle school, my attention and self-control were relatively poor,
    and I couldn't control some of my behaviors. For example,
    I was preparing to program, but in the end,
    I still did some things that made me more relaxed.
    Sometimes I was very motivated to solve some difficult problems,
    whether it was programming or courses,
    but sometimes I didn't want to do anything.
    Sometimes I couldn't get interested in computers, homework, and everything else.
    I just wanted to lose consciousness and no longer have any contact with this world.
I really can't figure out what my 'bright' future will look like.
    There are mountains outside the mountains, people outside,
    and people who are much more powerful than me. Can I live the life I want?
    I feel that there is a high probability that there is no hope.
I have been relatively introverted since elementary school,
    and by the time I reached middle school,
    although I looked lively around my classmates...
    I had nothing to say. I really wanted a friend,
    and my classmates and I could only say that we were "familiar",
    but I wanted a friend who could talk and chat with me anytime.
    I could show him/her everything without reservation.
    I "once" had such a friend, and we talked about everything,
    but someone deprived me of the right to do so.
    Who can still be considered my friend now?
I am now back to the way I used to be, but
I really hope to go back to the real past, cherish the things I want to cherish,
    and accompany the people I want to be with. But how could I have this opportunity?
I can only do my 'studio' and my studies well now.
    I must do this. All upstream buildings are determined by the underlying economic foundation.
    I have nothing to offer, including programming.
    I can only create a so-called 'virus' to promote myself.
    It's best if everything goes as I expected, hahaha......
I really want to cry now, I really want someone to comfort me, to accompany me.
I... I'm sorry to everyone who loves me, loved me,
    because my emotional intelligence prevents me from showing my gratitude in front of them.
It's really sad. This virus is finished.
I originally wanted to say these words to the people I wanted to say,
    but now I don't have the chance. I can only confide my heart to the computer,
    confide in my painstaking works, and let my works inherit my worthless thoughts and values!
After the virus runs,
I will commit suicide, whether to cut my wrists or hang myself.
    I will not be able to live forever, but I will try it all again,
    not necessarily to die. It is best to die,
    because I can see the prosperity of China,
    but I always remain pessimistic about my personal future.
    Sometimes because some causes will become idealism,
    I think that my hope is the world and the future,
    but the ideal and reality are always conflicting.
    Someone is destroying the idealist's dream.
    What I want to say to this person is:
        "Let the idealist immerse in the ideal foam,
         you don't have to hurry, and soon the foam
         will turn into an illusion..."
    I hope that what I dream is true,
    How I wish I lived in my dream,
    I wish I could live in a place full of hope,
    live hopeful days, and have a hopeful future... but is this possible?
T4.1.0 was written by me after iterating through three versions,
which really took my life. My current situation is that a serious illness is brewing,
and minor illnesses keep recurring. I wish I hadn't called, said that word, or cried.
Anyway, I don't plan to live much longer.
It's not a big deal to say more, and the subtitles can be longer.
Today is the year of Python (Snake), and this virus was created by Python.
    I wish you all the best not to follow my dead end.
    I wish you all good physical and mental health, study hard and excel like Xin, and
    I wish you all the best.
    I wish you all the best and success!
    Wishing you an ideal!
    Wishing you all academic ideals while sitting and standing!
    Career ideals!
    Long live idealism~\ (≥ ▽≤)/~!"""
        for i in ENDTEXT.split("\n"):
            _ = self.add_column(width=800, height=13, topspace=1)
            tk.Label(_, text=i, fg="white", bg="black", font=("System", 12)).pack(side=tk.LEFT)

        self.add_space(50)



        self.frame_window = self.canvas.create_window(screen_width // 2, 2500,
                                                      window=self.credits_frame, anchor=tk.CENTER)
        self.scroll_credits()

    def add_column(self, width=800, height=170, topspace=0, boothspace=0):
        if topspace: self.add_space(topspace)
        _ = tk.Frame(self.credits_frame, bg="black", width=width, height=height)
        _.pack_propagate(0)
        _.pack()
        if boothspace: self.add_space(boothspace)
        return _

    def add_space(self, size=50):
        tk.Label(self.credits_frame, text="\n", fg="white", bg="black", font=("", size)).pack()

    def scroll_credits(self):
        x, y = self.canvas.coords(self.frame_window)
        y -= 1
        self.canvas.coords(self.frame_window, x, y)

        if y + self.credits_frame.winfo_height() > 0:
            self.root.after(5, self.scroll_credits)
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    scroller = CreditsScroller(root)
    root.mainloop()