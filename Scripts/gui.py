from tkinter import *
from tkinter import messagebox
import tkinter.font
from main import main

# 전역 변수
global school_num

class Fonts:
    def font1(self):
        font1 = tkinter.font.Font(family="Consolas", size=20, weight="bold")
        return font1

    def font2(self):
        font2 = tkinter.font.Font(family="Consolas", size=12, weight="normal")
        return font2

    def font3(self):
        font2 = tkinter.font.Font(family="Consolas", size=12, weight="bold")
        return font2


class Buttons:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2
        self.is_pressed = False

    def button_press(self, event):
        if not self.is_pressed:
            self.run_btn.config(image=self.img2)
            self.is_pressed = True

    def button_release(self, event):
        if self.is_pressed:
            self.run_btn.config(image=self.img1)
            self.is_pressed = False


def button_click():
    global school_num
    param = entry.get()

    if param == "" or param == "ex) 3":
        messagebox.showwarning("경고", f"대기 시간을 입력해주세요.")
    else:
        try:
            param = float(param)
            if isinstance(param, float) and param >= 0:
                try:
                    print("school_num is ", school_num)
                    main(param, school_num)
                except:
                    messagebox.showwarning("경고", f"캠퍼스를 반드시 선택해주세요.")
            else:
                messagebox.showwarning("경고", f"대기 시간이 잘못되었습니다.\n param: {type(param)}")
        except:
            messagebox.showwarning("경고", f"대기 시간이 잘못되었습니다.\n param: {type(param)}")



def checkbox_clicked(checkbox):
    global school_num
    if checkbox == checkbox1:
        checkbox2.deselect()  # checkbox1이 선택되면 checkbox2는 선택 해제
        school_num = 1
    else:
        checkbox1.deselect()  # checkbox2가 선택되면 checkbox1은 선택 해제
        school_num = 2


def on_entry_click(event):
    if entry.get() == "ex) 3":  # 입력칸에 '3'이 있을 때만 삭제
        entry.delete(0, END)


def on_entry_focus_out(event):
    if entry.get() == "":  # 입력칸이 비어있을 때 초기값으로 '3' 설정
        entry.insert(0, "ex) 3")


window = Tk()

# Canvas 위젯 생성
canvas = Canvas(window, width=400, height=400)
canvas.pack()

window.title("연세 포탈 크롤러")
window.geometry("640x400+100+100")
window.resizable(True, True)

# 이미지 로드 및 변환
portal_logo = PhotoImage(file="images/yonsei_portal_logo.png").subsample(2)  # 이미지 파일 경로를 지정하세요
canvas.create_image(40.5, 0, anchor=NW, image=portal_logo)  # 이미지를 Canvas에 추가
yonsei_logo = PhotoImage(file="images/yonsei.png").subsample(3)
yonsei_breaked = PhotoImage(file="images/yonsei_breaked.png").subsample(3)


font = Fonts()
label2 = Label(window, text="학우님의 수강정보를 크롤링하여 엑셀시트로 정리하여 드립니다.", font=font.font2())
canvas.create_window(200, 150, window=label2)

label = Label(window, text="페이지 로딩 대기 시간 입력:")
canvas.create_window(50, 180, window=label)

entry = Entry(window, width=15, font=font.font2())
entry.insert(0, "ex) 3")  # 초기값으로 '3'을 입력
entry.config(fg="gray")  # 초기값 텍스트의 색상을 회색으로 지정
entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_entry_focus_out)
canvas.create_window(50, 200, window=entry)


button = Buttons(yonsei_logo, yonsei_breaked)
button.run_btn = Button(window, image=yonsei_logo)
button.run_btn.config(command=lambda: button_click())


button.run_btn.bind("<ButtonPress-1>", button.button_press)
button.run_btn.bind("<ButtonRelease-1>", button.button_release)

canvas.create_window(50, 290, window=button.run_btn)
label3 = Label(window, text="실행버튼", font=font.font3())
canvas.create_window(50, 375, window=label3)

var1 = IntVar()
var2 = IntVar()

checkbox1 = Checkbutton(window, text="신촌", variable=var1, onvalue=1, offvalue=0, font=font.font2(),
                        command=lambda: checkbox_clicked(checkbox1))
checkbox2 = Checkbutton(window, text="원주", variable=var2, onvalue=1, offvalue=0, font=font.font2(),
                        command=lambda: checkbox_clicked(checkbox2))

canvas.create_window(250, 200, window=checkbox1)
canvas.create_window(350, 200, window=checkbox2)

window.mainloop()



