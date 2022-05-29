# Translator

> **## 参考资料：**
>
> [pandas 读取excel、一次性写入多个sheet、原有文件追加sheet](https://blog.csdn.net/qq_35318838/article/details/104692846)
>
> [Pandas 获取EXCEL 各sheet name和内容的两种方法](https://blog.csdn.net/qq_35499652/article/details/120703525)
>
> [python入门-爬取百度翻译中的双语例句](https://www.jianshu.com/p/92478814d217)



1. 通过baidu翻译，爬取单词翻译，中文例句

   - test1.py 测试翻译的运行代码 

   - test2.py 测试自己的cookie和修改输入输出

   - test3.py 测试翻译句子

   - test.ipynb 学习文件读取，结果合并整理

2. 读取和写入修改一个excel文件的多个sheet

   ```python
   import pandas as pd
   
   res_df = pd.ExcelFile("./trans_res4.xlsx")
   raw_df = pd.ExcelFile("./RAW_data.xlsx")
   
   res_sheets = res_df.sheet_names
   raw_sheets = res_df.sheet_names
   
   from tqdm import trange
   
   for i  in trange(len(res_sheets)):
       na_res = res_sheets[i]
       na_raw = raw_sheets[i]
       print(na_res==na_raw)
   
   writer = pd.ExcelWriter("./trans_res5.xlsx", mode="w")
   for i  in trange(len(res_sheets)):
       name = res_sheets[i]
       df_res = res_df.parse(sheet_name=name)
       df_raw = raw_df.parse(sheet_name=name)
   
       df_raw.iloc[2:, 2] =  df_res.iloc[:, 2]
       df_raw.iloc[2:, 4] =  df_res.iloc[:, 4]
       df_raw.iloc[2:, 5] =  df_res.iloc[:, 5]
   
       df_raw.to_excel(writer, sheet_name=name, index=None)
       writer.save()
   
   writer.close()    
   ```

   



