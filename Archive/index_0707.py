import requests
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import json
from functools import partial
import tkintermapview as tkmap

# 區域代碼對應表
area_mapping = {
    '中正區': 63000010,
    '大同區': 63000020,
    '中山區': 63000030,
    '萬華區': 63000040,
    '信義區': 63000050,
    '松山區': 63000060,
    '大安區': 63000070,
    '南港區': 63000080,
    '北投區': 63000090,
    '內湖區': 63000100,
    '士林區': 63000110,
    '文山區': 63000120
}

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.datas = self.read_json('Data/長照機構總表_雙北市.json')
        self.title("長照機構資訊")

        self.areas = ['中正區', '大同區', '中山區', '萬華區',
                      '信義區', '松山區', '大安區', '南港區',
                      '北投區', '內湖區', '士林區', '文山區']

        self.container = tk.Frame(self)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.container.pack(side="left", fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_area_buttons()

        self.selected_area = None

    def create_area_buttons(self):
        self.button_frame = tk.Frame(self.scrollable_frame, bd=2, relief=tk.GROOVE, padx=10, pady=7)
        button_font = Font(family='微軟正黑體', size=12)
        for index, area in enumerate(self.areas):
            button = tk.Button(self.button_frame, text=area, font=button_font, bg="#D7C4BB", fg="#6A4028", padx=5, pady=8,
                               command=partial(self.show_message, area))
            button.pack(side=tk.LEFT, padx=5)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

    def show_message(self, area):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        back_button = tk.Button(self.scrollable_frame, text="返回", command=self.show_all_areas)
        back_button.pack(anchor=tk.W, pady=5)

        area_code = area_mapping.get(area)
        print(f"Selected area: {area}, area code: {area_code}")  # 调试信息
        filtered_data = [data for data in self.datas if data['區'] == area_code]
        print(f"Filtered data count: {len(filtered_data)}")  # 调试信息

        if filtered_data:
            message = f"**{area}** 的長照機構資訊：\n\n"
            message_label = tk.Label(self.scrollable_frame, text=message, justify=tk.LEFT, font=Font(family='微軟正黑體', size=12))
            message_label.pack(anchor=tk.W)

            for data in filtered_data:
                print(f"Data: {data}")  # 调试信息
                info = f"機構名稱：{data['機構名稱']}\n地址：{data['地址全址']}"
                info_label = tk.Label(self.scrollable_frame, text=info, justify=tk.LEFT, font=Font(family='微軟正黑體', size=12))
                info_label.pack(anchor=tk.W)
                map_button = tk.Button(self.scrollable_frame, text="查看地圖", command=lambda lat=data['緯度'], lon=data['經度'], address=data['地址全址']: self.show_map(lat, lon, address))
                map_button.pack(anchor=tk.W, pady=5)
        else:
            message = f"找不到 {area} 的長照機構資訊"
            message_label = tk.Label(self.scrollable_frame, text=message, justify=tk.LEFT, font=Font(family='微軟正黑體', size=12))
            message_label.pack(anchor=tk.W)

    def show_all_areas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_area_buttons()

    def show_map(self, lat, lon, address):
        if lat and lon:
            map_window = tk.Toplevel(self)
            map_window.title("地圖")
            map_frame = ttk.Frame(map_window)
            map_widget = tkmap.TkinterMapView(map_frame,
                                              width=800,
                                              height=600,
                                              corner_radius=0)
            map_widget.pack()
            map_widget.set_marker(lat, lon, text=address)
            map_widget.set_position(lat, lon)
            map_frame.pack(expand=True, fill='both')
            print(f"Added marker for {address} at ({lat}, {lon})")
        else:
            print(f"Could not get coordinates for {address}")

    def read_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as fileObject:
                data = json.load(fileObject)
                return data
        except Exception as e:
            print("讀取錯誤:", e)
            return None

if __name__ == "__main__":
    window = Window()
    window.geometry("800x600")
    window.mainloop()
