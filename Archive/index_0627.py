import requests
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import csv
from functools import partial
import tkintermapview as tkmap

LOCATIONIQ_API_KEY = "pk.b0b1f31b5d46487158d1b472af1faaba"

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.datas = self.read_csv("01.csv")
        self.title("長照機構資訊")

        self.areas = ['中正區', '大同區', '中山區', '萬華區',
                      '信義區', '松山區', '大安區', '南港區',
                      '北投區', '內湖區', '士林區', '文山區']

        self.message_frame = tk.Frame(self)
        self.message_frame.pack(side=tk.BOTTOM, padx=10, pady=10, anchor=tk.W)

        self.selected_area = None

        self.button_frame = tk.Frame(self, bd=2, relief=tk.GROOVE, padx=10, pady=7)
        button_font = Font(family='微軟正黑體', size=12)
        for index, area in enumerate(self.areas):
            button = tk.Button(self.button_frame, text=area, font=button_font, bg="#D7C4BB", fg="#6A4028", padx=5, pady=8,
                               command=partial(self.show_message, area))
            button.pack(side=tk.LEFT, padx=5)
        self.button_frame.pack(side=tk.TOP, padx=10, pady=10)

    def show_message(self, area):
        for widget in self.message_frame.winfo_children():
            widget.destroy()

        filtered_data = [data for data in self.datas if data[1] == area]

        if filtered_data:
            message = f"**{area}** 的長照機構資訊：\n\n"
            message_label = tk.Label(self.message_frame, text=message, justify=tk.LEFT, font=Font(family='微軟正黑體', size=12))
            message_label.pack(anchor=tk.W)

            for data in filtered_data:
                info = f"序號：{data[0]}\n機構名稱：{data[3]}\n地址：{data[10]}"
                info_label = tk.Label(self.message_frame, text=info, justify=tk.LEFT, font=Font(family='微軟正黑體', size=12))
                info_label.pack(anchor=tk.W)
                map_button = tk.Button(self.message_frame, text="點擊查看地圖", command=partial(self.show_map, data[10]))
                map_button.pack(anchor=tk.W)
        else:
            print(f"No data found for area: {area}")

        self.selected_area = area

    def show_map(self, address):
        coords = self.get_coordinates(address)
        if coords:
            # Initialize map widget
            map_window = tk.Toplevel(self)
            map_window.title("地圖")
            map_frame = ttk.Frame(map_window)
            map_widget = tkmap.TkinterMapView(map_frame,
                                              width=800,
                                              height=600,
                                              corner_radius=0)
            map_widget.pack()
            map_widget.set_marker(coords[0], coords[1], text=address)
            map_widget.set_position(coords[0], coords[1])
            map_frame.pack(expand=True, fill='both')
            print(f"Added marker for {address} at {coords}")
        else:
            print(f"Could not get coordinates for {address}")

    def read_csv(self, fileName):
        try:
            with open(fileName, 'r', encoding='utf8') as fileObject:
                csvReaderObject = csv.reader(fileObject)
                next(csvReaderObject)

                data = []
                for row in csvReaderObject:
                    data.append(row)

                return data
        except Exception as e:
            print("讀取錯誤:", e)
            return None

    def get_coordinates(self, address):
        try:
            response = requests.get(f'https://us1.locationiq.com/v1/search.php?key={LOCATIONIQ_API_KEY}&q={address}&format=json')
            response.raise_for_status()
            data = response.json()
            if data:
                return (float(data[0]['lat']), float(data[0]['lon']))
            else:
                print(f"No coordinates found for address: {address}")
                return None
        except requests.RequestException as e:
            print("HTTP error:", e)
            return None
        except ValueError as e:
            print("Value error:", e)
            return None
        except Exception as e:
            print("Unexpected error:", e)
            return None

if __name__ == "__main__":
    window = Window()
    window.geometry("+50+50")
    window.mainloop()
