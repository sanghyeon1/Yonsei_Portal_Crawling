from tkinter import *
from tkinter import messagebox
import tkinter.font
from main import main


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
    param = entry.get()
    if param == "":
        messagebox.showwarning("경고", f"대기 시간을 입력해주세요.")
    else:
        param = float(param)
        if isinstance(param, float) and param >= 0:
            print(param)
            main(param)
        else:
            messagebox.showwarning("경고", f"대기 시간이 잘못되었습니다.\n param: {type(param)}")


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
canvas.create_window(50, 200, window=entry)


button = Buttons(yonsei_logo, yonsei_breaked)
button.run_btn = Button(window, image=yonsei_logo)
button.run_btn.config(command=lambda: button_click())


button.run_btn.bind("<ButtonPress-1>", button.button_press)
button.run_btn.bind("<ButtonRelease-1>", button.button_release)

canvas.create_window(50, 290, window=button.run_btn)
label3 = Label(window, text="실행버튼", font=font.font3())
canvas.create_window(50, 375, window=label3)

window.mainloop()



