# ----------------------------------------------------
#             疫情自动填报（NWPU）版
#                     -----------由协和工作室开发
# ----------------------------------------------------
import requests
import lxml.html
import json
import datetime

login_url = 'https://uis.nwpu.edu.cn/cas/login'
ncov_url = 'http://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp'

def login(session, username, password):
    res = session.get(login_url)
    
    # 设置cookie信息
    cookies_dict = requests.utils.dict_from_cookiejar(res.cookies)
    assert cookies_dict['JSESSIONID'] and cookies_dict['sessoinMapKey']
    cookies = 'JSESSIONID={}; sessoinMapKey={}'.format(cookies_dict['JSESSIONID'], cookies_dict['sessoinMapKey'])
    session.headers.update({'Cookie':cookies})
    
    login_tree = lxml.html.fromstring(res.content)
    # 获取表单信息
    lt = login_tree.cssselect('input[name=lt]')[0].attrib['value']
    imageCodeName = ''
    errors = 0
    _eventId = 'submit'
    # 提交表单信息
    res = session.post(login_url, {
        'username':username,
        'password':password,
        'imageCodeName':imageCodeName,
        'errors':errors,
        'lt':lt,
        '_eventId':'submit'
    })

    # print(res.text)
    if '账号激活' not in res.text:
        return True
    return False

def post_ncov(session, username, place):
    headers = {
        'Referer': 'http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp'
    }
    res = session.post(ncov_url, data={
        'actionType': 'addRbxx',
        'userLoginId': username,
        'szcsbm': 3,
        'szcsmc': place,
        'sfjt': 0,
        'sfjtsm': '',
        'sfjcry': 0,
        'sfjcrysm': '',
        'sfjcqz': 0,
        'sfyzz': 0,
        'sfqz': 0,
        'ycqksm': '',
        'glqk': 0,
        'glksrq': '',
        'gljsrq': '',
        'tbly': 'sso'
    }, headers=headers)
    if  json.loads(res.text)['state'] == 1:
        return True
    return False

if __name__ == '__main__':
    username = None # 学号
    password = None # 密码
    place = None  # 地址

    print('---------------------欢迎使用疫情自动填报（NWPU版）---------------------')
    if not username:
        username = input('请输入你的学号：')
    if not password:
        password = input('请输入你的密码：')
    if not place:
        place = input('请输入你所在的区域：')
    
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://uis.nwpu.edu.cn/cas/login'
        }
    session = requests.Session()    # 会话对象
    session.headers.update(headers)
    
    if login(session, username, password) and post_ncov(session, username, place):
        today = datetime.datetime.now()
        print('学号为{}的同学你好，{}疫情已成功填报!'.format(username, today.strftime('%Y.%m.%d-%H:%M:%S')))
    else:
        print('填报失败，请检查学号，密码是否输错，或者网络是否连接！！')