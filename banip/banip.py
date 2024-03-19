#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time, os, re, ctypes, sys, datetime

File_Path = r"D:\4S\Pal\Binaries\Win64\logs"  # 帕鲁服务器反作弊日志文件夹路径 (这里要改)
File_IP_Cache = r"\\192.168.4.1\Gateway\PAL_DATA\Cache\\"  #允许登录的玩家路径,应该设置为login模块(这里要改)
File_Name_Cache = ".\\Cache\\"
Exit_Name_T = r'\d{2}:\d{2}:\d{2} (.*?) has logged out'  # exit
Join_SteamID_T = r'(\d{17})\] has logged in with IP'  # id
Join_IP_T = r'has logged in with IP.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
Join_Name_T = r'\d{2}:\d{2}:\d{2} (.*?) \[\d{17}\] has logged in with IP'  # name
rstr = r"[\/\\\:\*\?\"\<\>\|\s]"  # '/ \ : * ? " < > |'
PAL_Log_Path = ".\\PAL_Log\\"  # 服务器日志文件
PAL_Login_Log_Path = r'\\192.168.4.1\Gateway\PAL_DATA\\Login_LOG\\'  # 错误登录日志文件


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def banip(IP):
    Fire_Command = "netsh advfirewall firewall add rule name=\"PAL_Black_" + IP + "\" dir=in action=block protocol=UDP remoteip=" + IP

    if is_admin():
        if os.system(Fire_Command) == 0:
            print('封禁成功', IP)
    else:
        if sys.version_info[0] == 3:
            print("无管理员权限")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


def Jbanip(IP):
    Fire_Command = "netsh advfirewall firewall delete rule name=\"PAL_Black_" + IP + "\""
    if is_admin():
        if os.system(Fire_Command) == 0:
            print('解封成功', IP)
    else:
        if sys.version_info[0] == 3:
            print("无管理员权限")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


while (1 == 1):
    Time_HHMM = datetime.datetime.now()  # 获取当前时分秒
    Time_data = datetime.date.today()  # 获取当前日期

    File_Lists = os.listdir(File_Path)  # 获取目录下所有文件
    File_Lists.sort(key=lambda x: os.path.getmtime((File_Path + "\\" + x)))  # 按照文件修改时间排序
    try:
        File_New_Path = os.path.join(File_Path, File_Lists[-1])  # 获取最后修改的文件路径
    except:
        time.sleep(8)
        continue

    # -------------------开始解析日志文件-------------------
    Open_Log_File = open(File_New_Path, 'r', encoding='UTF-8')
    for Line in Open_Log_File:
        Join_IP = re.search(Join_IP_T, Line)  # 获取玩家加入游戏时候的IP的地址
        Join_Name = re.search(Join_Name_T, Line)  # 获取玩家加入时候的用户名
        Join_SteamID = re.search(Join_SteamID_T, Line)  # 获取玩家加入时候的steamid
        Exit_Name = re.search(Exit_Name_T, Line)  # 获取玩家退出时候的用户名

        if Join_SteamID != None:
            try:
                guolv_id = re.sub(rstr, "_", Join_Name.group(1))
                File_IP_Cache_Path = File_IP_Cache + Join_SteamID.group(1)
            except:
                banip(Join_IP.group(1))
                print('------------------封禁用户名不合法用户!-----------------------')
                continue
            try:
                File_IP_Cache_Path_Open = open(File_IP_Cache_Path, 'r', encoding='UTF-8')
                if File_IP_Cache_Path_Open.read() == Join_IP.group(1):
                    File_IP_Cache_Path_Open.close()

                    File_Name_Cache_Path = File_Name_Cache + guolv_id
                    File_Name_Cache_Path_Open = open(File_Name_Cache_Path, 'w', encoding='UTF-8')
                    File_Name_Cache_Path_Open.write(Join_IP.group(1))  # 将正常登录的用户名对应IP
                    File_Name_Cache_Path_Open.close()
                    print(Line, '--------------------正常登录--------------------')

                else:
                    print('------------------------IP错误玩家:' + Join_IP.group(1) + '--用户名:' + Join_Name.group(
                        1) + '---stamid:' + Join_SteamID.group(1))
                    IP_login_LOG = '日期:' + str(Time_HHMM) + '-----SteamID:' + Join_SteamID.group(
                        1) + '-----IP:' + Join_IP.group(1)
                    PAL_Login_Log_Path_steamid = PAL_Login_Log_Path + Join_SteamID.group(1)
                    PAL_Login_Log_Path_Open = open(PAL_Login_Log_Path_steamid, 'a', encoding='UTF-8')
                    PAL_Login_Log_Path_Open.write(IP_login_LOG + '\n')  # 将错误登录写入文件
                    PAL_Login_Log_Path_Open.close()
                    try:
                        File_Name_Cache_Path = File_Name_Cache + guolv_id
                        File_Name_Cache_Path_Open = open(File_Name_Cache_Path, 'w', encoding='UTF-8')
                        File_Name_Cache_Path_Open.write(Join_IP.group(1))  # 将非法玩家的用户名对应IP
                        File_Name_Cache_Path_Open.close()
                        banip(Join_IP.group(1))
                    except:
                        banip(Join_IP.group(1))
                        print('------------------封禁用户名不合法用户!-----------------------')
                        continue
            except FileNotFoundError:
                print('------------------------未登录玩家:' + Join_IP.group(1) + '------用户名:' + Join_Name.group(
                    1) + '------stamid:' + Join_SteamID.group(1))

                IP_login_LOG = '日期:' + str(Time_HHMM) + '-----SteamID:' + Join_SteamID.group(
                    1) + '-----IP:' + Join_IP.group(1)
                PAL_Login_Log_Path_steamid = PAL_Login_Log_Path + Join_SteamID.group(1)
                PAL_Login_Log_Path_Open = open(PAL_Login_Log_Path_steamid, 'a', encoding='UTF-8')
                PAL_Login_Log_Path_Open.write(IP_login_LOG + '\n')  # 将错误登录写入文件
                PAL_Login_Log_Path_Open.close()

                try:
                    File_Name_Cache_Path = File_Name_Cache + guolv_id
                    File_Name_Cache_Path_Open = open(File_Name_Cache_Path, 'w', encoding='UTF-8')
                    File_Name_Cache_Path_Open.write(Join_IP.group(1))  # 将非法玩家的用户名对应IP
                    File_Name_Cache_Path_Open.close()
                    banip(Join_IP.group(1))
                except:
                    banip(Join_IP.group(1))
                    print('------------------封禁用户名不合法用户!-----------------------')
                    continue
        # print(Exit_Name)
        if Exit_Name != None:
            exit_guolv_id = re.sub(rstr, "_", Exit_Name.group(1))
            File_Name_Cache_Path = File_Name_Cache + exit_guolv_id
            try:
                File_Name_Cache_Path_Open = open(File_Name_Cache_Path, 'r', encoding='UTF-8')
                ipip = File_Name_Cache_Path_Open.read()
                print(File_Name_Cache_Path, '<-解封文件.解封ip->', ipip)
                Jbanip(ipip)  # 玩家退出则通过用户名解除ip封禁
            except:
                print("删除失败：", File_Name_Cache_Path)
            try:
                File_Name_Cache_Path_Open.close()
            except:
                print()

    Open_Log_File.seek(0)  # 返回文件头
    Open_New_Log_FileName = PAL_Log_Path + str(Time_data) + ".txt"  # 拼接日志文件
    Open_New_Log_File = open(Open_New_Log_FileName, 'a', encoding='UTF-8')  # 将日志写入指定文件
    Open_New_Log_File.write(Open_Log_File.read())  # 将日志写入指定文件
    Open_Log_File.close()  # 关闭服务器日志文件
    Open_New_Log_File.close()  # 关闭本脚本日志文件
    os.remove(File_New_Path)

    time.sleep(8)
