import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showinfo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from tkinter import ttk
from sklearn.ensemble import RandomForestRegressor

# 讀取CSV檔案
data_path = '統計表.csv'
data = pd.read_csv(data_path).head(20)

# 建立主視窗
root = tk.Tk()
root.title("長照機構數據分析")
root.geometry("1700x500")
root.option_add("*Font", "新細明體 12")

# 顯示CSV資料的函數
def show_data():
    for i, col in enumerate(data.columns):
        tree.heading(f"#{i+1}", text=col)
        tree.column(f"#{i+1}", stretch=tk.YES, minwidth=100, width=120)
    
    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))

# 按鈕函數
def show_statistics():
    d = pd.DataFrame(data, columns=['地區','地區人口數','地區65up人口','65up長照需求人數','老化指數','扶老比','就業人口','薪資中位數','醫療院所數','照服人力','長照機構數'])
    stats = d.describe().round(6)

    stats_window = tk.Toplevel(root)
    stats_window.title("敘述統計表")
    stats_window.geometry("1500x200")

    # 建立新的 Treeview 來顯示統計表
    stats_tree = ttk.Treeview(stats_window, columns=list(stats.columns), show='headings')
    stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for i, col in enumerate(stats.columns):
        stats_tree.heading(f"#{i+1}", text=col)
        stats_tree.column(f"#{i+1}", stretch=tk.YES, minwidth=100, width=120)

    for index, row in stats.iterrows():
        stats_tree.insert("", "end", values=list(row))

    stats_scrollbar = ttk.Scrollbar(stats_window, orient=tk.VERTICAL, command=stats_tree.yview)
    stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    stats_tree.config(yscrollcommand=stats_scrollbar.set)

def show_scatter_matrix():
    plt.figure("散佈矩陣圖")
    scatter_matrix(data, figsize=(11,11))
    plt.show()

def show_box_plot():
    plt.figure("盒鬚圖")
    plt.boxplot(data['長照機構數'], showmeans=True)
    plt.title('長照機構數')
    plt.show()

def show_distribution():
    plt.figure("分佈圖")
    sns.distplot(data['長照機構數'], kde=True)
    plt.show()

def show_heatmap():
    plt.figure("熱力圖")
    numeric_df = data.select_dtypes(include=['number'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
    plt.show()

def show_random_forest_regression():
    numeric_df = data.select_dtypes(include=['number'])
    X = numeric_df.drop('長照機構數', axis=1)
    y = numeric_df['長照機構數']

    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_

    plt.figure("隨機森林回歸")
    plt.barh(X.columns, importances, align='center')
    plt.xlabel('特徵重要性')
    plt.title('隨機森林回歸 - 特徵重要性')
    plt.show()

# 表格顯示區
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame, columns=list(data.columns), show='headings')
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.config(yscrollcommand=scrollbar.set)

# 設定背景顏色
style = ttk.Style()
style.configure("Treeview", background="#E8E8E8", fieldbackground="#E8E8E8", font=("微軟正黑體", 12))
style.configure("Treeview.Heading", font=("微軟正黑體", 12))

# 加入按鈕
buttons_frame = tk.Frame(root)
buttons_frame.pack(padx=10, pady=10)

btn_statistics = tk.Button(buttons_frame, text="敘述統計表", command=show_statistics, font=("微軟正黑體", 12), width=12)
btn_statistics.grid(row=0, column=0, padx=15, pady=10)

btn_scatter_matrix = tk.Button(buttons_frame, text="散佈矩陣圖", command=show_scatter_matrix, font=("微軟正黑體", 12), width=12)
btn_scatter_matrix.grid(row=0, column=1, padx=15, pady=10)

btn_box_plot = tk.Button(buttons_frame, text="盒鬚圖", command=show_box_plot, font=("微軟正黑體", 12), width=12)
btn_box_plot.grid(row=0, column=2, padx=15, pady=10)

btn_distribution = tk.Button(buttons_frame, text="分佈圖", command=show_distribution, font=("微軟正黑體", 12), width=12)
btn_distribution.grid(row=0, column=3, padx=15, pady=10)

btn_heatmap = tk.Button(buttons_frame, text="熱力圖", command=show_heatmap, font=("微軟正黑體", 12), width=12)
btn_heatmap.grid(row=0, column=4, padx=15, pady=10)

btn_random_forest = tk.Button(buttons_frame, text="隨機森林回歸", command=show_random_forest_regression, font=("微軟正黑體", 12), width=12)
btn_random_forest.grid(row=0, column=5, padx=15, pady=10)

# 顯示CSV資料
show_data()

# 主循環
root.mainloop()
