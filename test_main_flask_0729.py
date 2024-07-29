import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from flask import Flask

# 建立 Flask 伺服器
server = Flask(__name__)

# 建立 Dash 應用程式
app = dash.Dash(__name__, server=server)

# 讀取 CSV 檔案
df = pd.read_csv(r'C:\Users\user\Documents\GitHub\TVDI_Project_LTC\Data\長照機構總表_for Flask.csv')

# 檢查行政區欄位的值，並去除 NaN
df = df.dropna(subset=['行政區'])

# 調試輸出，檢查行政區欄位的唯一值
print(df['行政區'].unique())

# 建立 Dash 佈局
app.layout = html.Div([
    html.H1("長照機構資訊"),
    dcc.Dropdown(
        id='area-dropdown',
        options=[{'label': area, 'value': area} for area in df['行政區'].unique()],
        value=df['行政區'].unique()[0] if len(df['行政區'].unique()) > 0 else None
    ),
    dash_table.DataTable(
        id='institution-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])

# 更新資料表的回呼函數
@app.callback(
    Output('institution-table', 'data'),
    [Input('area-dropdown', 'value')]
)
def update_table(selected_area):
    if selected_area:
        filtered_df = df[df['行政區'] == selected_area]
        return filtered_df.to_dict('records')
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
