import tkinter as tk
import tkinter.ttk as ttk
from finlab.data import Data
from my_strategy import my1,my2
import os
from tkinter import messagebox
import matplotlib as plt
# 起手式
from finlab.backtest import backtest
import datetime

#確認data
data = Data()

choose_window = tk.Tk()
choose_window.title("TonyStock選股系統")
choose_window.geometry('600x400')
msg = tk.StringVar()

welcome_msg = tk.Label(choose_window,text="請選擇交易策略 : ", width=15, height=1, font=7).grid(row=0, column=0)

def btn1_click():
    #每次點擊都先清空一次
    result_list.delete(0,tk.END)
    #記錄選擇的策略
    if myoptionmenu.get()==option_list[0]:
        strategy_summit = my1.packout(data)   
    elif myoptionmenu.get()==option_list[1]:
        strategy_summit = my2.packout(data) 
        
    
    #依選擇的策略呈現提示訊息
    if myoptionmenu.get()=="":
        msg.set("請選擇策略~")
        pass
    else:
        msg.set(myoptionmenu.get()+"的選取結果 : ")
    for item in strategy_summit:
        result_list.insert(tk.END, item)
    

        
def btn3_click():
    res = messagebox.askquestion("Confirm", "確定要離開嗎?")
    if res == "yes":
        choose_window.destroy()
        os.system("python tk01.py")
    else:
        pass
    

#下拉式選單
option_list = ['my1','my2']
#顯示所選的選單選項
myoptionmenu = ttk.Combobox(choose_window, value= option_list, state="readonly", width=15, height=1, font=7)
myoptionmenu .grid(row=0, column=1, sticky=tk.W)

#確定案紐(按下執行並顯示結果)
btn1 = tk.Button(choose_window, text="確定", command=btn1_click, state=tk.NORMAL, height=1, font=7)
btn1.grid(row=0, column=2, sticky=tk.N, padx=5)

# #提示
# show_choice = tk.Label(choose_window, textvariable=msg, font=3, relief="groove", width=13)
# show_choice.grid(row=1, column=0, pady=18)

#顯示成果
result_list = tk.Listbox(choose_window, font=7)
#此處pack要分開寫，不然會被視為Nonetype
result_list.grid(row=2, column=0)

def showSelected():
    show.config(text=result_list.curselection())
    
show = tk.Label(choose_window)
show.grid(row=2, column=1)
    
show_btn = tk.Button(choose_window, text='show select',command=showSelected)
show_btn.grid(row=2, column=2)

#離開按鈕
btn3 = tk.Button(choose_window, text="返回首頁", command=btn3_click, font=7)
btn3.place(anchor='center',relx=0.9, rely=0.92)

#畫圖
import matplotlib.pyplot as plt
from talib import abstract
import pandas as pd
import sqlite3
import os

# connect to sql
conn = sqlite3.connect(os.path.join('update_data', 'data', "data.db"))

# read data from sql
select_stock = '2330'
start ='2013-09-02'
end ='2020-3-31'

df = pd.read_sql('select stock_id, date, 開盤價, 收盤價, 最高價, 最低價, 成交股數 from price where stock_id='+'\"'+select_stock+'\"', conn,
                index_col=['date'], parse_dates=['date'])

# rename the columns of dataframe
df.rename(columns={'收盤價':'close', '開盤價':'open', '最高價':'high', '最低價':'low', '成交股數':'volume'}, inplace=True)

# 畫出均線
abstract.SMA(df).plot()

# 畫出收盤價
df['close'].plot()

# 創建各種指標
SMA = abstract.SMA(df)
RSI = abstract.RSI(df)
STOCH = abstract.STOCH(df)

from finlab.plot_candles import plot_candles
plot_candles(
              # 起始時間、結束時間
              start_time = start,
              end_time = end,
             
              # 股票的資料
              pricing=df, 
              title='Candles', 
    
              # 是否畫出成交量？
              volume_bars=True, 
    
              # 將某些指標（如SMA）跟 K 線圖畫在一起
              overlays=[SMA], 
    
              # 將某些指標（如RSI, STOCH）單獨畫在獨立的畫格中
              technicals = [RSI, STOCH],
    
              # 重新命名額外的畫格名稱（跟指標名稱一樣就可以囉！）
              technicals_titles=['RSI', 'KD']
            )



choose_window.mainloop()