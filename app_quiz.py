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
        self.quiz_num  =5
        self.isWrong = False
        self.wrong_num = 0
        #リザルト画面で次の問題番号を保持
        self.next_num = 0

    #問題の出題順序をバラバラに
    def difficulty(self,data):
        windows.destroy()
        windows.frame()
        windows.quiz_window(windows.new_frame)
        self.shuffle(data)
        self.show_quiz()

    def shuffle(self,data): 
        #間違えた問題があるか判定 
        self.isWrong = False
        #間違った問題の配列をリセット
        self.wrong_array = []
        #wrong_arrayの配列番号を保持
        self.wrong_num = 0
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

            for i in range(4):
                #選択肢表示
                windows.buttons[i].config(text= self.data_array[self.count][i],bg = "#FFFFFF",state =tk.NORMAL)
            #問題文表示
            photos.canvas.itemconfig(windows.lb_quiz,text= self.quiz_array[self.count]["Q"])
        else:
            windows.destroy()
            windows.frame()
            #結果を表示(Windowクラスに移動)
            windows.result(self.correct,self.quiz_num)
    
    #回答後のリザルト表示、numは問題を一つ後or一つ前に切り替えるために使う
    def show_result(self,num):
        quiz_num = 0
        select_num = 0
        ans_num = 0
        #次の問題（前へor次へを押したときの問題番号）
        self.next_num = self.wrong_array[self.wrong_num][0] + num
        print(self.next_num)
        if 0 <=  self.next_num and self.next_num < len(self.wrong_array):
            if num >= 0:
                self.wrong_num += 1
            elif num < 0:
                self.wrong_num -= 1        
           
        elif  self.next_num < 0:
            self.wrong_num = len(self.wrong_array) - 1

        elif self.next_num >= len(self.wrong_array):
            self.wrong_num = 0
        #quiz_num = 問題番号、select_num = 選んだ選択肢、ans_num = 正解の選択肢
        quiz_num = self.wrong_array[self.wrong_num][0]
        select_num = self.wrong_array[self.wrong_num][1]
        ans_num =  self.wrong_array[self.wrong_num][2]
        
        for i in range(4):
            #選択肢表示
            windows.lbs[i].config(text= self.data_array[quiz_num][i],bg = "#FFFFFF")
            if i == select_num:
                windows.lbs[select_num].config(bg = "#FF0000")
                
            if i == ans_num:

                windows.lbs[ans_num].config(bg = "#00FF00")
                #問題文表示
        photos.canvas.itemconfig(windows.lb_quiz,text= self.quiz_array[quiz_num]["Q"])

    #正解か判定する、numは選択したボタン
    def judge_ans(self,num):
        for button in windows.buttons:
            button.config(state=tk.DISABLED)
        ans = self.quiz_array[self.count]["ans"]
        self.choice = self.data_array[self.count][num]
        if self.choice == ans:
            windows.buttons[num].config(bg = "#00FF00")
            #正解数に＋１する
            self.correct += 1
            windows.roots.after(1000, self.next_question)

        else:
            #一度でも間違えればフラグ発動（結果画面でボタンを表示させるため）
            self.isWrong = True
            
            windows.buttons[num].config(bg = "#FF0000")
            
            #for button in windows.buttons:でも良いが正解のボタン番号が欲しいのでi in range を使う
            for i in range(4):
                #cget("text")でそれぞれのボタンのテキスト情報を取得して正解のボタンがどれかを見つける
                if windows.buttons[i].cget("text") == ans:
                    windows.buttons[i].config(bg = "#00FF00")

                    #間違った問題の番号、自分の選択肢、正解のボタンを保存
                    wrong_num = [self.count,num,i]

                    #保存した問題を配列に入れる（[[問題番号,選択した番号],[問題番号,選択した番号],....]の2次元配列になるイメージ）
                    self.wrong_array.append(wrong_num)
            windows.roots.after(1000, self.next_question)

            #ボタン操作で次の問題に進みたいなら↓の３行、時間経過で次の問題に進むなら↑の１行
            
            # windows.roots.bind("<KeyPress>",self.press)
    # def press(self,event):
    #         windows.roots.after(1000, self.next_question)

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
        photos.make_photo(windows.new_frame,"bg_select.png",500,500)

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

    def quiz_window(self,frame):
        photos.make_photo(frame,"bg.png",500,500)
        #wraplengthでボタンに表示されるテキストの長さを制限（自動で改行）
        #cursor="hand2"でカーソルの形を変えています。"hand2"の部分に入れられるものは数多くあり、
        #その種類は"xterm"（Iの字になるやつ）等の、よく見るものから
        #"star"(☆の形になる)等の初めて見るものまであります。詳しくは調べてみてね
        self.bt_op1 = tk.Button(frame, text="0",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(0),cursor = "hand2")
        self.bt_op1.place(x = 20,y = 200)
        self.bt_op2 = tk.Button(frame,text="1",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(1),cursor = "hand2")
        self.bt_op2.place(x = 20,y = 350)
        self.bt_op3 = tk.Button(frame,text="2",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(2),cursor = "hand2")
        self.bt_op3.place(x = 250,y = 200)
        self.bt_op4 = tk.Button(frame,text="3",width=17,height=5, wraplength=190,font = ("MSゴシック","17"),command=lambda:files.judge_ans(3),cursor = "hand2")
        self.bt_op4.place(x = 250,y = 350)

        self.buttons = [self.bt_op1, self.bt_op2, self.bt_op3, self.bt_op4]

        #問題文を表示、widthの値は一行にどれくらいの長さの文字（文字数ではなく文字列全体の長さ）まで入れられるか（超えると次の行が生まれる）
        self.lb_quiz = photos.canvas.create_text(230,80,text="問題",fill = "#000000",font = ("MSゴシック","15","bold"),anchor=tk.CENTER,width=400)

    def result_window(self,frame):
        photos.make_photo(frame,"bg.png",500,500)
        #wraplengthでボタンに表示されるテキストの長さを制限（自動で改行）
        #cursor="hand2"でカーソルの形を変えています。"hand2"の部分に入れられるものは数多くあり、
        #その種類は"xterm"（Iの字になるやつ）等の、よく見るものから
        #"star"(☆の形になる)等の初めて見るものまであります。詳しくは調べてみてね
        self.lb1 = tk.Label(frame, text="0",width=17,height=5,bg = "#ffffff" ,wraplength=190,font = ("MSゴシック","17"))
        self.lb1.place(x = 20,y = 200)
        self.lb2 = tk.Label(frame,text="1",width=17,height=5,bg = "#ffffff" ,wraplength=190,font = ("MSゴシック","17"))
        self.lb2.place(x = 20,y = 350)
        self.lb3 = tk.Label(frame,text="2",width=17,height=5,bg = "#ffffff" ,wraplength=190,font = ("MSゴシック","17"))
        self.lb3.place(x = 250,y = 200)
        self.lb4 = tk.Label(frame,text="3",width=17,height=5,bg = "#ffffff" ,wraplength=190,font = ("MSゴシック","17"))
        self.lb4.place(x = 250,y = 350)

        self.lbs = [self.lb1, self.lb2, self.lb3, self.lb4]

        #問題文を表示、widthの値は一行にどれくらいの長さの文字（文字数ではなく文字列全体の長さ）まで入れられるか（超えると次の行が生まれる）
        self.lb_result = photos.canvas.create_text(230,80,text="問題",fill = "#000000",font = ("MSゴシック","15","bold"),anchor=tk.CENTER,width=400)

    def start_window(self):
        #画像読み込み
        photos.make_photo(windows.new_frame,"bg_title.png",500,500)
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
        photos.make_photo(windows.new_frame,"bg_result.png",500,500) 
        
        #正解率
        rate = int(correct * 100 ) // whole
        photos.canvas.create_text(250,150,text = "リザルト",font = ("MSゴシック","40","bold"))
        photos.canvas.create_text(250,220,text = "正解数：" + str(correct) + "/" + str(whole),font = ("MSゴシック","30"))
        photos.canvas.create_text(250,270,text = "正解率：" + str(rate) + "%" ,font = ("MSゴシック","30"))
        bt_restart = tk.Button(self.new_frame,text="タイトルに戻る",fg = "#FFFFFF",bg= "#05002E",width=15,height=2,font = ("MSゴシック","20"),command=back,cursor = "hand2")
        bt_restart.place(x = 150,y = 400)

        #間違えた問題があったときのみボタンを表示
        if files.isWrong:
            bt = tk.Button(self.new_frame,text="間違えた問題",bg= "#FFFEE4",width=15,height=2,font = ("MSゴシック","20"),command=self.review,cursor = "hand2")
            bt.place(x = 150,y = 300)


    #arrayは間違えた問題の番号とその時に選んだ回答を含む配列
    def review(self):
        #一番最初に間違えた問題にする
        files.wrong_num = 0
        
        #別画面を作成
        review_window = tk.Toplevel(self.roots)
        review_window.geometry("500x500")
        review_window.resizable(False,False)

        self.result_window(review_window)
       
        files.show_result(0)

        bt_prev = tk.Button(review_window,text="前へ",bg= "#FFFEE4",width=10,height=2,font = ("MSゴシック","10"),command=lambda:files.show_result(-1),cursor = "hand2")
        bt_prev.place(x = 10,y = 20)
        bt_next = tk.Button(review_window,text="次へ",bg= "#FFFEE4",width=10,height=2,font = ("MSゴシック","10"),command=lambda:files.show_result(1),cursor = "hand2")
        bt_next.place(x = 420,y = 20)
        
class Photo:
    def __init__(self):
        self.photo_cache = []

    #roots=
    def make_photo(self,roots,name,width,height):
        self.roots  = roots
        self.width = width
        self.height = height
        self.load_name = name
        self.load_photo()
        self.make_canvas(self.roots)
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
    
    def make_canvas(self,frame):
        self.canvas = tk.Canvas(frame,width= 500,height= 500)
        self.canvas.place(x=0,y=0)
    def put_photo(self,px,py):
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