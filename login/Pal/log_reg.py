import re, os, datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

steamid64_pattern = r'^7656\d{13}'  # 判断steamid格式的正则
password_pattern = r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$'  # 密码规则
username_pattern = r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{4,12}$'  # 用户名规则
File_User = '.\\DATA\\User\\'  # IP信息文件位置
File_IP = r'\\192.168.4.1\Gateway\PAL_DATA\\Cache\\'  # 登录之后玩家ip和steamid允许登录的玩家路径应该和banip模块路径一致   (这里要改)
IP_pattern = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'  # 匹配ip
Login_log = r'\\192.168.4.1\Gateway\PAL_DATA\Login_LOG\\'  #错误登录信息的文件保存 (这里要改)
Time_HHMM = datetime.datetime.now()  # 获取当前时分秒
Time_data = datetime.date.today()  # 获取当前日期
Login_status = False  # 是否公开注册
Login_Code = '778866qqaax'  # 注册码


def index_html(request):
    return render(request, 'index.html')


def login_html(request):
    return render(request, "login.html")


def register_html(request):
    if not Login_status:
        return render(request, 'register_false.html')
    return render(request, 'register.html')


def check_login_html(request):
    return render(request, 'check_login.html')


def register(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        logincode = request.POST.get('logincode')

        if Login_Code == logincode or Login_status == True:
            if password != '' and username != '':

                if not re.search(steamid64_pattern, username):
                    return HttpResponse("<h1><p style=\"text-align:center\">steamID64,格式错误</p></h1></br>"
                                        "<button onclick=\"window.location.href='../register.html'\" "
                                        "type=\"button\">返回注册</button>")
                elif not re.search(password_pattern, password):
                    return HttpResponse(
                        "<h1><p style=\"text-align:center\">密码格式错误,请输入6-16位的数字和字母(不能纯数字或字母)</p></h1></br>"
                        "<button onclick=\"window.location.href='../register.html'\" "
                        "type=\"button\">返回注册</button>")
                else:
                    File_User_Path = File_User + username
                    print(File_User_Path)
                    if os.path.exists(File_User_Path):
                        return HttpResponse(
                            "<h1><p style=\"text-align:center\">该steamid已被注册,如果被盗用请联系群主</p></h1></br>"
                            "<button onclick=\"window.location.href='../register.html'\" "
                            "type=\"button\">返回注册</button>")
                    else:
                        File_User_Path_Open = open(File_User_Path, 'w+', encoding='UTF-8')
                        if File_User_Path_Open.write(password):
                            File_User_Path_Open.close()
                            return HttpResponse("您绑定的用Steamid64是:" + username + "(这将是你的登录账号)" +
                                                "</br>您的密码是:" + password +
                                                "</br>请复制或截图妥善保存"
                                                "<button onclick=\"window.location.href='../login.html'\" "
                                                "type=\"button\">返回登录</button>")
                        else:
                            File_User_Path_Open.close()
                            return HttpResponse("注册失败联系群主")
            else:
                return HttpResponse("<h1><p style=\"text-align:center\">请同时输入正确的[密码,steamID64]缺一不可</p></h1></br>"
                                    "<button onclick=\"window.location.href='../register.html'\" "
                                    "type=\"button\">返回注册</button>")
        else:
            return HttpResponse("激活码错误,由于炸服挂捣乱暂不开放注册,需要注册请联系管理员")
            
    else:
        return HttpResponse("ERROR.不要用微信QQ等乱七八糟的内置浏览器访问,请打开谷歌浏览器等")


def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')

        ip_ip = request.POST.get('ip')
        print(ip_ip)
        File_User_Path = File_User + username

        try:
            File_User_Path_Open = open(File_User_Path, 'r', encoding='UTF-8')
            if File_User_Path_Open.read() == password:
                File_User_Path_Open.close()

                if ip_ip == '':

                    if request.META.get('HTTP_X_FORWARDED_FOR'):
                        ip = request.META.get("HTTP_X_FORWARDED_FOR")
                    else:
                        ip = request.META.get("REMOTE_ADDR")

                else:
                    if re.search(IP_pattern, ip_ip):
                        ip = ip_ip
                    else:
                        return HttpResponse("</br>IP格式错误</br>"
                                            "<button onclick=\"window.location.href='../login.html'\" "
                                            "type=\"button\">返回登录</button>")

                File_IP_Path = File_IP + username
                File_IP_Path_Open = open(File_IP_Path, 'w+', encoding='UTF-8')
                if File_IP_Path_Open.write(ip):
                    return HttpResponse(
                        "<h1><p style=\"text-align:center\">登录成功,您现在可以用IP:" + ip + "加入游戏了</p></h1></br>"
                                                                                             "<h1><p style=\"text-align:center\">无法加入游戏可能是你的浏览器挂了代理,或者游戏挂了加速器,如果你是自己输入的IP也许错了</p></h1></br>")
                else:
                    return HttpResponse('这个错误可能是服务端问题,请联系管理员')
            else:
                return HttpResponse('密码错误检查用户名,忘了找群主')
        except:
            return HttpResponse("<h1><p style=\"text-align:center\">steamid未注册请先点下方按钮注册</p></h1></br>"
                                "<button onclick=\"window.location.href='../register.html'\" "
                                "type=\"button\">返回注册</button>")
    else:
        return HttpResponse("ERROR.不要用微信QQ等乱七八糟的内置浏览器访问,请打开谷歌浏览器等")


def check_login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')
        File_User_Path = File_User + username

        try:
            File_User_Path_Open = open(File_User_Path, 'r', encoding='UTF-8')
            if File_User_Path_Open.read() == password:
                File_User_Path_Open.close()
                try:
                    Login_log_path = Login_log + username
                    print(Login_log_path)
                    Login_log_path_open = open(Login_log_path, 'r', encoding='UTF-8')

                    Line_return = ''
                    for Line in Login_log_path_open:
                        Line_return = Line_return + Line + '</br>'
                except:
                    return HttpResponse("没有登录记录")

                return HttpResponse(Line_return)
                Login_log_path_open.close()
            else:
                return HttpResponse('密码错误检查用户名,忘了找群主')
        except:
            return HttpResponse("<h1><p style=\"text-align:center\">steamid未注册请先点下方按钮注册</p></h1></br>"
                                "<button onclick=\"window.location.href='../register.html'\" "
                                "type=\"button\">返回注册</button>")
    else:
        return HttpResponse("ERROR.不要用微信QQ等乱七八糟的内置浏览器访问,请打开谷歌浏览器等")
