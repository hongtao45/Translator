
from getTranslation import getTranslation
from tqdm import trange

import pandas as pd


def main(words, result):
    
    data = pd.ExcelFile(words)
    writer = pd.ExcelWriter(result, mode='w') # a 已有文件添加 w 新建/覆盖 修改

    sheets = data.sheet_names
    col = ["Term", "中文翻译", "英文例句", "中文例句"]
    for name in sheets:
        df = data.parse(sheet_name= name)
        vobs = df.iloc[:, 0] # 第一列
        lines = []  # 最终结果的行
        
        tqdm_rang = trange(len(vobs))
        tqdm_rang.set_description(desc=name)
        for i in tqdm_rang: # 每个单词
            vob = vobs[i]
            res_dict = getTranslation(vob)
            line = [""] * 4
            
            if len(res_dict["zh_res"]) == 0:
                line[0] = vob
                # print("==0") # 测试了，会进到这里面的 之前的 try except 触发过
            else:
                len_liju =len(res_dict['liju_zh'])
                if  len_liju >= 1:
                    line[0] = vob
                    line[1] = res_dict["zh_res"]
                    line[2] = res_dict["liju_en"][0] 
                    line[3] = res_dict['liju_zh'][0] 
                else:
                    line[0] = vob
                    line[1] = res_dict["zh_res"]
                    # line[2] = res_dict["liju_en"][0] 
                    # line[3] = res_dict['liju_zh'][0]

            lines.append(line)
        
        data_res = pd.DataFrame(lines, columns=col)
        data_res.to_excel(writer, sheet_name=name, index=None)
        writer.save()

    writer.close()


if __name__ == '__main__':

    # 正式代码
    words =r"./RAW_data.xlsx"
    result = r"./trans_res.xlsx"
    main(words, result)
