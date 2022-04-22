import pandas as pd
from finlab.data import Data
from collections import defaultdict

global allstocklist  
allstocklist = []
稅後淨利 = Data().get('本期淨利（淨損）', 1)
for i in 稅後淨利.keys():
    allstocklist.append(i)
    
data = Data()
     
def strategy(data):
    #成長性:月營收成長、營收較去年同月成長 、毛利較去年同期上升(成長率)，以上條件前300強
    #籌碼面:成交筆數>350
    #安全性:流動比率>1     
          
    #月營收成長
    月營收成長 = data.get('上月比較增減(%)',1)
    月營收成長 = 月營收成長.iloc[-1].sort_values(ascending=False)
    #存取為pandas.series為了最後結尾輸出
    condition1 = pd.Series(True,index=月營收成長[:300].index)
        
    #營收較去年同月成長 
    營收較去年同月成長 = data.get('去年同月增減(%)',1)   
    營收較去年同月成長 = 營收較去年同月成長.iloc[-1].sort_values(ascending=False)
    #存取為pandas.series為了最後結尾輸出
    condition2 = pd.Series(True,index=營收較去年同月成長[:300].index)
        
    #毛利成長率
    毛利 = data.get('營業毛利（毛損）淨額',5)
    毛利較去年同期上升 = ((毛利.iloc[-1])-(毛利.iloc[-5]))/毛利.iloc[-5]
    毛利較去年同期上升 = 毛利較去年同期上升.sort_values(ascending=False)
    #存取為pandas.series為了最後結尾輸出
    condition3 = pd.Series(True,index=毛利較去年同期上升[:300].index)
    
    #成交筆數
    成交筆數 = data.get('成交筆數',1)
    成交量 = 成交筆數.iloc[-1]
    condition4 = 成交量>350
        
    #流動比率
    流動資產 = data.get('流動資產合計',1)
    流動負債 = data.get('流動負債合計',1)
    流動比率 = 流動資產.iloc[-1]/流動負債.iloc[-1]
    condition5 = 流動比率>1
     
    #收尾
    condition = condition1 & condition2 & condition3 & condition4 & condition5
    return condition[condition]
    
 