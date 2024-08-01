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

# 讀取 CSV 檔案，使用原始字符串（在字符串前加 r）
df = pd.read_csv(r'C:\Users\user\Documents\GitHub\TVDI_Project_LTC\Data\長照機構總表_for Flask.csv')

# 檢查縣市和行政區欄位的值，並去除 NaN
df = df.dropna(subset=['縣市', '行政區'])

# 建立 Dash 佈局
app.layout = html.Div([
    html.H1("長照機構資訊"),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in df['縣市'].unique()],
        value=df['縣市'].unique()[0] if len(df['縣市'].unique()) > 0 else None
    ),
    dcc.Dropdown(
        id='area-dropdown'
    ),
    dash_table.DataTable(
        id='institution-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])

# 更新行政區選項的回呼函數
@app.callback(
    Output('area-dropdown', 'options'),
    [Input('city-dropdown', 'value')]
)
def set_area_options(selected_city):
    if selected_city:
        filtered_df = df[df['縣市'] == selected_city]
        return [{'label': area, 'value': area} for area in filtered_df['行政區'].unique()]
    return []

# 更新行政區選項的預設值
@app.callback(
    Output('area-dropdown', 'value'),
    [Input('area-dropdown', 'options')]
)
def set_area_value(available_options):
    if available_options:
        return available_options[0]['value']
    return None

# 更新資料表的回呼函數
@app.callback(
    Output('institution-table', 'data'),
    [Input('city-dropdown', 'value'),
     Input('area-dropdown', 'value')]
)
def update_table(selected_city, selected_area):
    if selected_city and selected_area:
        filtered_df = df[(df['縣市'] == selected_city) & (df['行政區'] == selected_area)]
        return filtered_df.to_dict('records')
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
