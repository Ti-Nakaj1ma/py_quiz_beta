import json
import tkinter as tk
#下の行の”PIL”が波線になっている場合、pip install pillow等でpillowをインストールしてください
from PIL import Image,ImageTk
# from tkinter import messagebox
import random

def bt_enter(event):
    photos.canvas.itemconfig(photo_id1,image= img_bt2)
    root.config(cursor = "hand2")

def bt_leave(event):
    photos.canvas.itemconfig(photo_id1,image= img_bt1)
    root.config(cursor = "arrow")
#最初のスタートボタンをクリックしたときの処理
def bt_click(event):
    root.config(cursor = "arrow")
    select()

#難易度に応じた問題を呼び出す
def easy():
    files.difficulty(data1)
def normal():
    files.difficulty(data2)
def hard():
    files.difficulty(data3)
def veryhard():
    files.difficulty(data4)

def select():
    windows.destroy()
    windows.frame()
    windows.select_window()
def back():
    windows.destroy()
    windows.frame()
    windows.start_window()

#問題を出す色々な機能を担当
class Files:
    def __init__(self):
        #一回で何問出すか
        self.quiz_num  =25
    #問題の出題順序をバラバラに
    def difficulty(self,data):
        windows.destroy()
        windows.frame()
        windows.quiz_window()
        self.shuffle(data)
        self.show_quiz()

    def shuffle(self,data):
        random.shuffle(data)
        self.quiz_array = data
        length = len(data)

        self.data_array = []
        #選択肢をバラバラに
        for i in range(length):
            random.shuffle(data[i]["op"])
            self.data_array.append(data[i]["op"])
        #何問目かを保存
        self.count = 0
        #正解数を保存
        self.correct = 0

    
    def show_quiz(self):
        if self.count < self.quiz_num:
            self.buttons = [windows.bt_op1, windows.bt_op2, windows.bt_op3, windows.bt_op4]

            for i in range(4):
                self.buttons[i].config(text= self.data_array[self.count][i],bg = "#FFFFFF",state =tk.NORMAL)

            photos.canvas.itemconfig(windows.lb_quiz,text= self.quiz_array[self.count]["Q"])
        else:
            windows.destroy()
            windows.frame()
            #結果を表示(Windowクラスに移動)
            windows.result(self.correct,self.quiz_num)

    def judge_ans(self,num):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        ans = self.quiz_array[self.count]["ans"]
        self.choice = self.data_array[self.count][num]
        if self.choice == ans:
            self.buttons[num].config(bg = "#00FF00")
            #正解数に＋１する
            self.correct += 1
            windows.roots.after(1000, self.next_question)

        else:
            self.buttons[num].config(bg = "#FF0000")
            # for button in self.buttons:
            #     #cget("text")でそれぞれのボタンのテキスト情報を取得して正解のボタンがどれかを見つける
            #     if button.cget("text") == ans:
            #         button.config(bg = "#00FF00")
            windows.roots.bind("<KeyPress>",self.press)
    def press(self,event):
            windows.roots.after(1000, self.next_question)

    def next_question(self):
        self.count += 1
        self.show_quiz()

class Window:
    def __init__(self,roots):
        self.roots = roots  
    def destroy(self):
        self.new_frame.destroy()
    def frame(self):
        self.new_frame = tk.Frame(self.roots, width=500,height=500)
        self.new_frame.place(x=0,y=0)

    def select_window(self):
        photos.make_photo("bg_select.png",500,500)

        bt_easy = tk.Button(self.new_frame, text="簡単",height=1,width=10,font = ("MSゴシック","20"),command=easy ,cursor = "hand2")
        bt_easy.place(x = 190,y = 100)
        bt_normal = tk.Button(self.new_frame,text="普通",height=1,width=10,font = ("MSゴシック","20"),command=normal,cursor = "hand2")
        bt_normal.place(x = 190,y = 200)
        bt_hard = tk.Button(self.new_frame,text="難問",height=1,width=10,font = ("MSゴシック","20"),command=hard,cursor = "hand2")
        bt_hard.place(x = 190,y = 300)
        bt_veryhard = tk.Button(self.new_frame,text="超難問",height=1,width=10,font = ("MSゴシック","20"),command=veryhard,cursor = "hand2")
        bt_veryhard.place(x = 190,y = 400)

        bt_back = tk.Button(self.new_frame,text="戻る",height=2,width=5,font = ("MSゴシック","20"),command=back,cursor = "hand2")
        bt_back.place(x = 20,y = 20)

    def quiz_window(self):
        photos.make_photo("bg.png",500,500)
        #wraplengthでボタンに表示されるテキストの長さを制限（自動で改行）
        #cursor="hand2"でカーソルの形を変えています。"hand2"の部分に入れられるものは数多くあり、
        #その種類は"xterm"（Iの字になるやつ）等の、よく見るものから
        #"star"(☆の形になる)等の初めて見るものまであります。詳しくは調べてみてね
        self.bt_op1 = tk.Button(self.new_frame, text="0",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(0),cursor = "hand2")
        self.bt_op1.place(x = 20,y = 200)
        self.bt_op2 = tk.Button(self.new_frame,text="1",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(1),cursor = "hand2")
        self.bt_op2.place(x = 20,y = 350)
        self.bt_op3 = tk.Button(self.new_frame,text="2",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(2),cursor = "hand2")
        self.bt_op3.place(x = 250,y = 200)
        self.bt_op4 = tk.Button(self.new_frame,text="3",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(3),cursor = "hand2")
        self.bt_op4.place(x = 250,y = 350)

        #問題文を表示、widthの値は一行にどれくらいの長さの文字（文字数ではなく文字列全体の長さ）まで入れられるか（超えると次の行が生まれる）
        self.lb_quiz = photos.canvas.create_text(230,80,text="問題",fill = "#000000",font = ("MSゴシック","15","bold"),anchor=tk.CENTER,width=400)
    def start_window(self):
        #画像読み込み
        photos.make_photo("bg_title.png",500,500)
        # 
        photos.make_button_photo("button2.png",100,50)

        img_bt1 = photos.make_button_photo("button1.png",100,50)
        photo_id1 = photos.canvas.create_image(200,300,image = img_bt1, anchor=tk.NW)

        text_id = photos.canvas.create_text(250,325,text = "スタート",font = ("MSゴシック","20"))

        photos.canvas.tag_bind(photo_id1,"<Enter>",bt_enter)
        photos.canvas.tag_bind(photo_id1,"<Leave>",bt_leave)
        photos.canvas.tag_bind(photo_id1,"<Button-1>",bt_click)
        photos.canvas.tag_bind(text_id,"<Enter>",bt_enter)
        photos.canvas.tag_bind(text_id,"<Leave>",bt_leave)
        photos.canvas.tag_bind(text_id,"<Button-1>",bt_click)

    def result(self,correct, whole):
        photos.make_photo("bg_result.png",500,500) 
        #正解率
        rate = int(correct * 100 ) // whole
        photos.canvas.create_text(250,150,text = "リザルト",font = ("MSゴシック","40","bold"))
        photos.canvas.create_text(250,220,text = "正解数：" + str(correct) + "/" + str(whole),font = ("MSゴシック","30"))
        photos.canvas.create_text(250,270,text = "正解率：" + str(rate) + "%" ,font = ("MSゴシック","30"))
        bt = tk.Button(self.new_frame,text="タイトルに戻る",bg= "#FFFEE4",width=15,height=2,font = ("MSゴシック","20"),command=back,cursor = "hand2")
        bt.place(x = 150,y = 300)

class Photo:
    def __init__(self):
        self.photo_cache = []

    def make_photo(self,name,width,height):
        self.width = width
        self.height = height
        self.load_name = name
        self.load_photo()
        self.put_photo(0,0)
    def make_button_photo(self,name,width,height):
        self.width = width
        self.height = height
        self.load_name = name
        self.load_photo()
        return self.new_photo
    def load_photo(self):
        image = Image.open(self.load_name)
        image = image.resize((self.width,self.height))
        image = ImageTk.PhotoImage(image)
        self.photo_cache.append(image)
        self.new_photo = image
    
    def put_photo(self,px,py):
        self.canvas = tk.Canvas(windows.new_frame,width= 500,height= 500)
        self.canvas.place(x=0,y=0)
        self.canvas.create_image(px,py,image = self.new_photo, anchor=tk.NW)


root = tk.Tk()
#選択画面を作る

root.geometry("500x500")
root.title("新！pythonマスターへの道")
#ウィンドウサイズを固定
root.resizable(False, False)

#jsonファイルを開く
file1 = open("question_easy.json",encoding="utf-8")
data1=json.load(file1)
file2 = open("question_normal.json",encoding="utf-8")
data2=json.load(file2)
file3 = open("question_hard.json",encoding="utf-8")
data3=json.load(file3)
file4 = open("question_veryhard.json",encoding="utf-8")
data4=json.load(file4)

windows = Window(root)
windows.frame()
photos = Photo()
files = Files()

windows.start_window()
img_bt2 = photos.make_button_photo("button2.png",100,50)

img_bt1 = photos.make_button_photo("button1.png",100,50)
photo_id1 = photos.canvas.create_image(200,300,image = img_bt1, anchor=tk.NW)

text_id = photos.canvas.create_text(250,325,text = "スタート",font = ("MSゴシック","20"))

photos.canvas.tag_bind(photo_id1,"<Enter>",bt_enter)
photos.canvas.tag_bind(photo_id1,"<Leave>",bt_leave)
photos.canvas.tag_bind(photo_id1,"<Button-1>",bt_click)
photos.canvas.tag_bind(text_id,"<Enter>",bt_enter)
photos.canvas.tag_bind(text_id,"<Leave>",bt_leave)
photos.canvas.tag_bind(text_id,"<Button-1>",bt_click)


file1.close()
file2.close()
file3.close()
file4.close()

root.mainloop()