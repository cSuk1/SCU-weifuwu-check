import requests
import datetime
import json
from urllib.parse import urlparse, parse_qs
import os


# url参数转化成字典
def url_to_dict(url):
    # 提取url参数
    query = urlparse(url).query
    # 将字符串转换为字典
    # 所得的字典的value都是以列表的形式存在，若列表中都只有一个值
    params = parse_qs(query)
    result = {key: params[key][0] for key in params}
    return result


# 判断是否已经写入数据
size = os.path.getsize('config/config.json')

# 当已经写入
if size > 0:
    # 读取config中的数据
    with open("config/config.json", 'r') as load_f:
        # 读取json
        load_dict = json.load(load_f)
        Ucookie = load_dict['Ucookie']
        data = load_dict['data']
        conten_len = load_dict['content_length']
        # 更新实时时间
        time = now = datetime.datetime.now()
        time = time.strftime('%Y%m%d')
        time = int(time) - 1
        time = str(time)
        data["data"] = time
    load_f.close()
else:
    # 否则先配置
    eai_sess = input("请设置eai_sess：")
    UUkey = input("请设置UUkey：")
    Hm_lvt_48b682d4885d22a90111e46b972e3268 = input("请设置Hm_lvt_48b682d4885d22a90111e46b972e3268：")
    Hm_lpvt_48b682d4885d22a90111e46b972e3268 = input("请设置Hm_lpvt_48b682d4885d22a90111e46b972e3268：")
    post_data = input("请输入传递的参数：")
    cookie = "eai-sess=" + eai_sess + "; UUkey=" + UUkey + "; Hm_lvt_48b682d4885d22a90111e46b972e3268=" + Hm_lvt_48b682d4885d22a90111e46b972e3268 + "; Hm_lpvt_48b682d4885d22a90111e46b972e3268=" +  Hm_lpvt_48b682d4885d22a90111e46b972e3268
    # udata = url_to_dict("https://exp.com/?" + post_data)
    udata = json.loads(post_data)
    data_dict = {
        "Ucookie": cookie,
        "content_length": length,
        "data": udata
    }
    # 写入缓存
    with open("config/config.json", 'w') as write_f:
        json.dump(data_dict, write_f, indent=4, ensure_ascii=False)

    # 读取config中的数据
    with open("config/config.json", 'r') as load_f:
        load_dict = json.load(load_f)
        Ucookie = load_dict['Ucookie']
        conten_len = load_dict['content_length']
        data = load_dict['data']


url = 'https://wfw.scu.edu.cn/ncov/wap/default/save'

# 请求头
headers = {
    'Host': 'wfw.scu.edu.cn',
    'Cookie': Ucookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '3000',
    'Origin': 'https://wfw.scu.edu.cn',
    'Referer': 'https://wfw.scu.edu.cn/ncov/wap/default/index?from=historyhttps://www.baidu.com/?tn=15007414_pg',
    'Sec-Fetch-Des': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Te': 'trailers',
    'Connection': 'close'
}

headers['Content-Length'] = str(len(str(data)) + len(str(headers)))

response = requests.post(url=url, data=data, headers=headers)

if response.status_code == 200:
    print('打卡成功！')
    print(response.text)
else:
    print('打卡失败！')
    print(response.text)
