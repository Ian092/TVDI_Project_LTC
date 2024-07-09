import requests  # type: ignore
import tkinter as tk
from tkinter.font import Font
import csv


class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.datas = self.read_csv("01.csv")
        self.title("長照機構資訊")


        self.areas = ['中正區', '大同區', '中山區', '萬華區',
                      '信義區', '松山區', '大安區', '南港區',
                      '北投區', '內湖區', '士林區', '文山區']

        
        self.message_label = tk.Label(self, text="", font=Font(family='微軟正黑體', size=12))
        self.message_label.pack(side=tk.BOTTOM, padx=10, pady=10, anchor=tk.W) 

        self.selected_area = None

        self.button_frame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=7)
        button_font = Font(family='微軟正黑體', size=12)
        for index, area in enumerate(self.areas):
            button = tk.Button(self.button_frame, text=area, font=button_font, bg="#D7C4BB", fg="#6A4028", padx=5, pady=8,
                               command=lambda area=area: self.show_message(area))  
            button.pack(side=tk.LEFT, padx=5)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

    def show_message(self, area):

        filtered_data = [data for data in self.datas if data[1] == area]
        self.message_label.config(text="")

        if filtered_data:
            message = f"**{area}** 的長照機構資訊：\n\n"
            for data in filtered_data:
                message += f"序號：{data[0]}\n"
                message += f"機構名稱：{data[3]}\n"
                message += f"地址：{data[10]}\n\n"
            self.message_label.config(text=message, justify=tk.LEFT)  
        self.selected_area = area

   

    def read_csv(self, fileName):
        try:
            fileObject = open(fileName, 'r', encoding='utf8')
            csvReaderObject = csv.reader(fileObject)
            next(csvReaderObject)

            data = []
            for row in csvReaderObject:
                data.append(row)

            fileObject.close()
            return data
        except Exception as e:
            print("讀取錯誤")
            fileObject.close()
            return None


if __name__ == "__main__":
    window = Window()
    window.geometry("+50+50")
    window.mainloop()
