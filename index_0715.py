import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import json

# 讀取 JSON 文件
with open('長照機構總表_雙北市.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 將資料分成台北市和新北市
taipei_data = [item for item in data if item['縣市'] == 63000]
new_taipei_data = [item for item in data if item['縣市'] == 65000]

# 獲取所有行政區域
taipei_districts = list(set(item['區'] for item in taipei_data))
new_taipei_districts = list(set(item['區'] for item in new_taipei_data))

# 初始化 Tkinter
root = tk.Tk()
root.title("長照機構地圖")
root.geometry("800x600")

# 創建地圖
map_widget = TkinterMapView(root, width=800, height=500, corner_radius=0)
map_widget.pack(fill="both", expand=True)
map_widget.set_position(25.03746, 121.5637)  # 中心點設置在台北市
map_widget.set_zoom(10)

# 創建城市選單
def update_districts(event):
    city = city_var.get()
    if city == "台北市":
        district_menu['values'] = taipei_districts
        district_var.set('')
    elif city == "新北市":
        district_menu['values'] = new_taipei_districts
        district_var.set('')

def show_institutions():
    district = district_var.get()
    if city_var.get() == "台北市":
        institutions = [item for item in taipei_data if item['區'] == district]
    else:
        institutions = [item for item in new_taipei_data if item['區'] == district]
    
    map_widget.delete_all_markers()
    for item in institutions:
        map_widget.set_marker(item['緯度'], item['經度'], text=item['機構名稱'])

city_var = tk.StringVar()
city_menu = ttk.Combobox(root, textvariable=city_var)
city_menu['values'] = ["台北市", "新北市"]
city_menu.pack(pady=10)
city_menu.bind('<<ComboboxSelected>>', update_districts)

# 創建行政區選單
district_var = tk.StringVar()
district_menu = ttk.Combobox(root, textvariable=district_var)
district_menu.pack(pady=10)

# 顯示按鈕
show_button = tk.Button(root, text="顯示機構", command=show_institutions)
show_button.pack(pady=10)

# 啟動主循環
root.mainloop()
