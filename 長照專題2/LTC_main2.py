import tkinter as tk
import os
from tkinter import messagebox
from tkinter.messagebox import showinfo
from matplotlib.font_manager import FontProperties
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from pandas.plotting import scatter_matrix
from tkinter import ttk
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split

# 讀取CSV檔案
data_path = '修改後的統計表.csv'
data = pd.read_csv(data_path).head(20)

# 設定字型路徑
font_path = 'C:/Windows/Fonts/msjh.ttc'  # 微軟正黑體的字型檔案路徑
font_properties = FontProperties(fname=font_path)

# 設定全局字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 建立主視窗
root = tk.Tk()
root.title("長照機構數據分析")
root.geometry("1700x500")
#root.option_add("*Font", "微軟正黑體 12")

# 顯示CSV資料的函數
def show_data():
    for i, col in enumerate(data.columns):
        tree.heading(f"#{i+1}", text=col)
        tree.column(f"#{i+1}", stretch=tk.YES, minwidth=100, width=120)
    
    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))

# 按鈕函數
def show_statistics():
    d = pd.DataFrame(data, columns=['地區','地區人口數','老年人口數','長照需求人數','老化指數','扶老比','就業人口','薪資中位數','醫療院所數','照服人力','長照機構數'])
    stats = d.describe().round(6)

    stats_window = tk.Toplevel(root)
    stats_window.title("統計表")
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

def show_bar_line_chart():
    window = tk.Toplevel(root)
    window.title("條形折線圖")

    regions = data['地區']
    long_term_care_facilities = data['長照機構數']
    population_65_up = data['長照需求人數']

    fig, ax1 = plt.subplots(figsize=(15, 8))
    ax1.set_xlabel('地區', fontproperties=font_properties)
    ax1.set_ylabel('長照機構數', color='tab:blue', fontproperties=font_properties)
    ax1.bar(regions, long_term_care_facilities, color='tab:blue', alpha=0.6, label='長照機構數')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('長照需求人數', color='tab:green', fontproperties=font_properties)
    ax2.plot(regions, population_65_up, color='tab:green', marker='o', label='長照需求人數')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    plt.title('地區的長照機構數和長照需求人數', fontproperties=font_properties)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_box_plot():
    window = tk.Toplevel(root)
    window.title("盒鬚圖")

    variables = ['地區人口數','老年人口數','長照需求人數','老化指數','扶老比','就業人口','薪資中位數','醫療院所數','照服人力','長照機構數']
    num_vars = len(variables)

    fig, axs = plt.subplots(2, 5, figsize=(20, 15))

    for i, var in enumerate(variables):
        row = i // 5
        col = i % 5
        axs[row, col].boxplot(data[var], vert=True, patch_artist=True, boxprops=dict(facecolor="lightblue"))
        axs[row, col].set_title(f'{var} 的盒鬚圖', fontproperties=font_properties)
        axs[row, col].set_ylabel(var, fontproperties=font_properties)
        axs[row, col].grid(True)

    # 調整佈局
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_actual_vs_predicted():
    window = tk.Toplevel(root)
    window.title("實際和預測圖")

    features = data[['地區人口數','老年人口數','長照需求人數','老化指數','扶老比','就業人口','薪資中位數','醫療院所數','照服人力']]
    predicted_values = model.predict(features)

    results = data[['地區', '長照機構數']].copy()
    results['預測長照機構數'] = predicted_values

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(results['地區'], results['長照機構數'], marker='o', color='#E9CD4C', label='實際長照機構數')
    ax.plot(results['地區'], results['預測長照機構數'], marker='x', color='#0089A7', label='預測長照機構數')

    ax.set_xlabel('地區', fontproperties=font_properties)
    ax.set_ylabel('長照機構數', fontproperties=font_properties)
    ax.set_title('各地區實際與預測長照機構數比較', fontproperties=font_properties)
    plt.xticks(rotation=45)
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_heatmap():
    window = tk.Toplevel(root)
    window.title("熱力圖")

    numeric_df = data.select_dtypes(include=['number'])
    fig, ax = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('相關係數熱力圖', fontproperties=font_properties)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_decision_tree():
    window = tk.Toplevel(root)
    window.title("決策樹圖")

    global model
    features = data[['地區人口數', '老年人口數', '長照需求人數', '老化指數', '扶老比', '就業人口', '薪資中位數', '醫療院所數', '照服人力']]
    target = data['長照機構數']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)

    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(model, feature_names=features.columns.tolist(), filled=True, rounded=True, fontsize=10, ax=ax)

    ax.set_title("長照機構數的決策樹", fontproperties=font_properties)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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

btn_statistics = tk.Button(buttons_frame, text="統計表", command=show_statistics, font=("微軟正黑體", 12), width=12)
btn_statistics.grid(row=0, column=0, padx=15, pady=10)

btn_bar_line_chart = tk.Button(buttons_frame, text="條形折線圖", command=show_bar_line_chart, font=("微軟正黑體", 12), width=12)
btn_bar_line_chart.grid(row=0, column=1, padx=15, pady=10)

btn_box_plot = tk.Button(buttons_frame, text="盒鬚圖", command=show_box_plot, font=("微軟正黑體", 12), width=12)
btn_box_plot.grid(row=0, column=2, padx=15, pady=10)

btn_heatmap = tk.Button(buttons_frame, text="熱力圖", command=show_heatmap, font=("微軟正黑體", 12), width=12)
btn_heatmap.grid(row=0, column=4, padx=15, pady=10)

btn_decision_tree = tk.Button(buttons_frame, text="決策樹圖", command=show_decision_tree, font=("微軟正黑體", 12), width=12)
btn_decision_tree.grid(row=0, column=5, padx=15, pady=10)

btn_actual_vs_predicted = tk.Button(buttons_frame, text="實際和預測圖", command=show_actual_vs_predicted, font=("微軟正黑體", 12), width=12)
btn_actual_vs_predicted.grid(row=0, column=6, padx=15, pady=10)

# 顯示CSV資料
show_data()

# 主循環
root.mainloop()
