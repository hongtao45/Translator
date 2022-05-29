
import requests
import json
import re
import execjs
import urllib
import time

def getTranslation_sentence(source = 'machine'):
    '''
    input:
        source: 待翻译的单词，句子
    output:
        res_zh      : str  中文结果
        liju_en_res : list 英文例句
        liju_zh_res : list 中文例句
    '''
    zh_res = ""


    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    #     "Cookie": "BAIDUID=4650B0B34048BBAA1E0B909B42F5A564:FG=1; BIDUPSID=4650B0B34048BBAA1E0B909B42F5A564; PSTM=1537177909; BDUSS=w0VmEzUFFWTTh0bld5VWVhNVo5MEEyV2ZKdTk3U2stMGZmWVQ1TTRuSnVkOHBiQVFBQUFBJCQAAAAAAAAAAAEAAAD0GzcNaG9uZ3F1YW4xOTkxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7qoltu6qJbTk; pgv_pvi=6774493184; uc_login_unique=19e6fd48035206a8abe89f98c3fc542a; uc_recom_mark=cmVjb21tYXJrXzYyNDU4NjM%3D; MCITY=-218%3A; cflag=15%3A3; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02893452711; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1539333192; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1539333307",
    # }

    # 请求头数据
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
        "Cookie": "BAIDUID=FCD8F779FC6F03FDE6B2A50EF68BBE27:SL=0:NR=10:FG=1; BAIDUID_BFESS=FCD8F779FC6F03FDE6B2A50EF68BBE27:SL=0:NR=10:FG=1; BDUSS=UlrWVhJcWhmVTZueHNueE1qNW4ybFlDT3ljMEdwd3E1MnVMN35KZGJTUEpBNmxpSVFBQUFBJCQAAAAAAAAAAAEAAABzmviVz~6357LQ1MK66QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMl2gWLJdoFiT; BDUSS_BFESS=UlrWVhJcWhmVTZueHNueE1qNW4ybFlDT3ljMEdwd3E1MnVMN35KZGJTUEpBNmxpSVFBQUFBJCQAAAAAAAAAAAEAAABzmviVz~6357LQ1MK66QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMl2gWLJdoFiT; H_WISE_SIDS=107314_110085_127969_132547_184716_185637_188333_194085_194519_194529_196428_197242_197711_198502_199022_199567_201193_203310_203880_203882_203885_204713_204715_204717_204720_204864_204901_205420_205424_206704_206928_207235_207697_207716_208001_208607_208721_208969_209063_209345_209395_209455_209568_209748_209846_210293_210665_210791_211018_211336_211351_211457_211476_211580_211691_211698_211735_211754_211952_212295_212617_212631_212701_212789_212798_212868_212969_213003_213031_213070_213094_213125_213218_213257_213272_213307_213355_213415_213565_213648_214002_214006_214025_214105_214135_214140_214231_214380_214535_214569_214655; ZFY=NhVlXVyuKFYy:ApitIhkRGjB7wlogpCi6uCYG4K:ALhmI:C; APPGUIDE_10_0_2=1; SOUND_SPD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1653736484,1653754318; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1653754398",
    }

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            "Cookie": "__yjs_duid=1_a0452d56ad8685026e7f2944ba55840f1642598559620; BCLID_BFESS=7959664467298922867; BDSFRCVID_BFESS=51_OJeCAa49V8-cDaZQnJdt8VgKK0gOTH6Hhl-aXvISp-X8VfByiEG0PMf8g0KuME_ZfogKKL2OTHmuF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbAqoCIXJIK3JRnYb-Qoq4D_MfOtetJyaR0tox7vWJ5TEJDmeqDWqttv-J6I2fTbbnbp0hvctn3cShPCy-7Sqt_R54rgbIrvfNch5tTV3l02Vh6Ie-t2ynLIQJnzKtRMW23roq7mWn6hsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKjG8jJjoP; BIDUPSID=FCD8F779FC6F03FDE6B2A50EF68BBE27; PSTM=1649382612; BAIDUID=FCD8F779FC6F03FDE6B2A50EF68BBE27:SL=0:NR=10:FG=1; BAIDUID_BFESS=FCD8F779FC6F03FDE6B2A50EF68BBE27:SL=0:NR=10:FG=1; BDUSS=UlrWVhJcWhmVTZueHNueE1qNW4ybFlDT3ljMEdwd3E1MnVMN35KZGJTUEpBNmxpSVFBQUFBJCQAAAAAAAAAAAEAAABzmviVz~6357LQ1MK66QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMl2gWLJdoFiT; BDUSS_BFESS=UlrWVhJcWhmVTZueHNueE1qNW4ybFlDT3ljMEdwd3E1MnVMN35KZGJTUEpBNmxpSVFBQUFBJCQAAAAAAAAAAAEAAABzmviVz~6357LQ1MK66QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMl2gWLJdoFiT; H_WISE_SIDS=107314_110085_127969_132547_184716_185637_188333_194085_194519_194529_196428_197242_197711_198502_199022_199567_201193_203310_203880_203882_203885_204713_204715_204717_204720_204864_204901_205420_205424_206704_206928_207235_207697_207716_208001_208607_208721_208969_209063_209345_209395_209455_209568_209748_209846_210293_210665_210791_211018_211336_211351_211457_211476_211580_211691_211698_211735_211754_211952_212295_212617_212631_212701_212789_212798_212868_212969_213003_213031_213070_213094_213125_213218_213257_213272_213307_213355_213415_213565_213648_214002_214006_214025_214105_214135_214140_214231_214380_214535_214569_214655; ZFY=NhVlXVyuKFYy:ApitIhkRGjB7wlogpCi6uCYG4K:ALhmI:C; APPGUIDE_10_0_2=1; SOUND_SPD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1653736484,1653754318; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1653754398; ab_sr=1.0.1_YzdmZTQ0OGZkOWVjZmJhOWZlZmYxMDBhMjIxNmEwZjk2YWJiOTc2ZTYyNDM5Njc1NTU0Zjg3MGZlYzExM2VkYTMxNTZhYjUxZjdkMDQyNDMwZTQwNWFmY2ZlOTVkMzYzMGM3OTUyNmVjNzI0ZDUzNmE1ZGJhM2IzZGEyYzVhOTZjMGNjYjU4YmUxYWQyMzQzZWQwN2U5NGY5ZDRkNWFlN2MwMWI4ZTgwNGQwYmE4MTg0NThmZTMyN2VjOTk4OGIy",
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
    # print('source = ' + source + ', sign = ' + sign)

    # 请求接口
    fromLanguage = 'en'
    toLanguage = 'zh'

    # 请求接口地址
    v2transapi = 'https://fanyi.baidu.com/v2transapi?from=%s&to=%s&query=%s' \
                 '&transtype=translang&simple_means_flag=3&sign=%s&token=%s' % (
                     fromLanguage, toLanguage, urllib.parse.quote(source), sign, token)

    # print(v2transapi)

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

    
    zh_res =result["trans_result"]["data"][0]["dst"]
    
    
    return zh_res


def test_trans():
    
    sentence = "application"
    res = getTranslation_sentence(sentence)
    print(res)


if __name__ == '__main__':
    
    # 测试翻译代码
    test_trans()