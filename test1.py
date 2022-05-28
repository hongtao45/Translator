import requests
import json
import re
import execjs
import urllib
import time

# 请求头非常重要，在请求 fanyi.baidu.com 这个页面的时候需要传递
# 笔者测试时发现，如果不传递的话百度也会返回 token 和 gtk，但是此时返回的值是无法正确请求到翻译结果的

#### gtk 好像都是 320305.131321201
#### token 是固定的，每台机器都不一样
#### sign 每次都是不一定的，通过一段js代码加密；
#### Cookie 每段时间都会变化；998、997 这些错误代码跟 Cookie 有关
#### 最重要的破解这个 sign，最后居然能直接通过 get 获得数据..




f_english = open("english.txt", "w+")
f_chinese = open("chinese.txt", "w+")
f_synonym = open("synonym.txt", "w+")


def getTranslation(source = 'machine'):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Cookie": "BAIDUID=4650B0B34048BBAA1E0B909B42F5A564:FG=1; BIDUPSID=4650B0B34048BBAA1E0B909B42F5A564; PSTM=1537177909; BDUSS=w0VmEzUFFWTTh0bld5VWVhNVo5MEEyV2ZKdTk3U2stMGZmWVQ1TTRuSnVkOHBiQVFBQUFBJCQAAAAAAAAAAAEAAAD0GzcNaG9uZ3F1YW4xOTkxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7qoltu6qJbTk; pgv_pvi=6774493184; uc_login_unique=19e6fd48035206a8abe89f98c3fc542a; uc_recom_mark=cmVjb21tYXJrXzYyNDU4NjM%3D; MCITY=-218%3A; cflag=15%3A3; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02893452711; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1539333192; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1539333307",
    }

    # 获取网页源码
    html = requests.get('https://fanyi.baidu.com', headers=headers)
    html.encoding = 'utf-8'

    # 正则匹配 gtk
    matches = re.findall("window.gtk = '(.*?)';", html.text, re.S)
    for match in matches:
        gtk = match

    if gtk == "":
        print('Get gtk fail.')
        exit()
    # print('gtk = ' + gtk)

    # 正则匹配 token
    matches = re.findall("token: '(.*?)'", html.text, re.S)
    for match in matches:
        token = match

    if token == "":
        print('Get token fail.')
        exit()
    # print('token = ' + token)

    # 计算 sign
    signCode = 'function a(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}var C=null;var hash=function(r,_gtk){var o=r.length;o>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(o/2)-5,10)+r.substr(-10,10));var t=void 0,t=null!==C?C:(C=_gtk||"")||"";for(var e=t.split("."),h=Number(e[0])||0,i=Number(e[1])||0,d=[],f=0,g=0;g<r.length;g++){var m=r.charCodeAt(g);128>m?d[f++]=m:(2048>m?d[f++]=m>>6|192:(55296===(64512&m)&&g+1<r.length&&56320===(64512&r.charCodeAt(g+1))?(m=65536+((1023&m)<<10)+(1023&r.charCodeAt(++g)),d[f++]=m>>18|240,d[f++]=m>>12&63|128):d[f++]=m>>12|224,d[f++]=m>>6&63|128),d[f++]=63&m|128)}for(var S=h,u="+-a^+6",l="+-3^+b+-f",s=0;s<d.length;s++)S+=d[s],S=a(S,u);return S=a(S,l),S^=i,0>S&&(S=(2147483647&S)+2147483648),S%=1e6,S.toString()+"."+(S^h)}'

    sign = execjs.compile(signCode).call('hash', source, gtk)
    print('source = ' + source + ', sign = ' + sign)

    # 请求接口
    fromLanguage = 'en'
    toLanguage = 'zh'

    # 请求接口地址
    v2transapi = 'https://fanyi.baidu.com/v2transapi?from=%s&to=%s&query=%s' \
                 '&transtype=translang&simple_means_flag=3&sign=%s&token=%s' % (
                     fromLanguage, toLanguage, urllib.parse.quote(source), sign, token)

    print(v2transapi)

    #### 最大重试次数
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            translate_result = requests.get(v2transapi, headers=headers)
            success = True
        except:
            attempts += 1
            if attempts == 3:
                break

    result = json.loads(translate_result.text)
    # print(translate_result.text)

    # print(result)
    # print('-----同义词-----')
    # if "sanyms" in dict(result["dict_result"]).keys():
    #     words = result["dict_result"]["sanyms"][0]["data"][0]["d"]
    #     for s in words:
    #         print(s, file=f_synonym)
    #         print(s)
    # else:
    #     print("----没有同义词----")

    print("翻译结果:{}".format(result["trans_result"]["data"][0]["dst"]))
    # print(lines)
    ### line: 每一组句子，包含一句中文和一句英文
    ### sentences: 每个句子
    ### sentence: 句子中的每个词；格式：['The', 'w_0', 'w_0', 0, ' ']

    print('-----双语例句-----')
    double = result["liju_result"]['double']
    if double != "":
        lines = json.loads(result["liju_result"]['double'])
        is_english = True
        for line in lines:
            # print(line)
            for sentences in line:
                # print(sentences)
                if isinstance(sentences, list):
                    s = ""
                    # print(sentences)
                    for i, sentence in enumerate(sentences): # 组词成句
                        if is_english:
                            if i > len(sentences) - 3:
                                s += sentence[0]
                            else:
                                s += sentence[0] + " "
                        else:
                            s += sentence[0]
                    
                    s.encode("gbk", 'ignore').decode("gbk", "ignore")
                    if is_english:
                        print(s, file=f_english)
                        print(s)
                        is_english = False
                    else:
                        print(s, file=f_chinese)
                        print(s)
                        is_english = True

                    # print(s)
                    # print()
                    s = ""

f_vob = open("electronic.txt")
for line in f_vob:
    source = line
    getTranslation(source)

f_vob.close()
f_english.close()
f_chinese.close()
f_synonym.close()

# entry = result["dict_result"]["collins"]["entry"]
# # print(entry)
# i = 1
# for e in entry:
#     # print(e)
#     for value in e["value"]:
#         # print(value)
#         mean_type = value.get('mean_type', '')
#         # print(mean_type)
#         for examples in mean_type:
#             # print(examples)
#             for example in examples.get('example', ''):
#                 # print(example)
#                 print('-----------    ' + str(i))
#                 ex = example["ex"]
#                 print(ex)
#                 tran = example["tran"]
#                 print(tran)
#                 i += 1
