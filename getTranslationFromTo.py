
import requests
import execjs
import re
import optparse

def get_options(args=None):
    optParser = optparse.OptionParser()
    optParser.add_option("-f", "--from", dest="fromL", default="en",
                        help="原始语言英文缩写")
    optParser.add_option('-t', '--to', dest='toL', default="zh", 
                        help="输出语言英文缩写")

    (options, args) = optParser.parse_args(args=args)
    return options
    

def translation(q_vob, options):
    url = 'https://fanyi.baidu.com/v2transapi'
    headers = {'cookie':'BAIDUID=4650B0B34048BBAA1E0B909B42F5A564:FG=1; BIDUPSID=4650B0B34048BBAA1E0B909B42F5A564; PSTM=1537177909; BDUSS=w0VmEzUFFWTTh0bld5VWVhNVo5MEEyV2ZKdTk3U2stMGZmWVQ1TTRuSnVkOHBiQVFBQUFBJCQAAAAAAAAAAAEAAAD0GzcNaG9uZ3F1YW4xOTkxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7qoltu6qJbTk; pgv_pvi=6774493184; uc_login_unique=19e6fd48035206a8abe89f98c3fc542a; uc_recom_mark=cmVjb21tYXJrXzYyNDU4NjM%3D; MCITY=-218%3A; cflag=15%3A3; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02893452711; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1539333192; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1539333307'}

    # 获取网页源码
    html = requests.get('https://fanyi.baidu.com', headers=headers)
    html.encoding = 'utf-8'
    
    # 正则匹配 token
    matches = re.findall("token: '(.*?)'", html.text, re.S)
    for match in matches:
        token = match


    js = '''var i = "320305.131321201"
    function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a : r << a, r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
    
    
    function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++) "" !== e[C] && f.push.apply(f, a(e[C].split(""))), C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
        }
        var u = void 0, l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i : (i = window[l] || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
        }
        for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b], p = n(p, F);
        return p = n(p, D), p ^= s, 0 > p && (p = (2147483647 & p) + 2147483648), p %= 1e6, p.toString() + "." + (p ^ m)
    }
    '''


    # 请求接口
    
    From = options.fromL
    To =  options.toL
    
    sign = execjs.compile(js).call("e",q_vob)
    data = {
        'from':From,
        'to':To,
        'query':q_vob,
        'sign':sign,
        'token':token}

    try:
        text = requests.post(url,headers=headers,data=data).json()['trans_result']['data'][0]['dst']
    except:
        text = f"{q_vob} 查询失败"
    
    return text


def test():
    q_vob = "Chinese authorities"

    args = ["-f","en", "-t", "cht"]
    options =get_options(args)
    
    text = translation(q_vob, options)
    print(text)


if __name__ == '__main__':
    test()
    