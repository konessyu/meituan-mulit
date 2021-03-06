#!coding: cp936
import win32ras
import time, os
from spider import *


def Connect(dialname, account, passwd):
    dial_params = (dialname, '', '', account, passwd, '')
    return win32ras.Dial(None, None, dial_params, None)


def DialBroadband():
    dialname = '宽带连接'  # just a name
    account = '宽带账号'
    passwd = '宽带密码'
    try:
        # handle is a pid, for disconnect or showipadrress, if connect success return 0.
        # account is the username that your ISP supposed, passwd is the password.
        handle, result = Connect(dialname, account, passwd)
        time.sleep(3)
        if result == 0:
            print("Connection success!")
            return handle, result
        else:
            print("Connection failed, wait for 5 seconds and try again...")
            time.sleep(5)
            DialBroadband()
    except:
        print( "Can't finish this connection, please check out.")
        return


def Disconnect(handle):
    if handle != None:
        try:
            win32ras.HangUp(handle)
            #防止程序执行过快，导致拨号失败
            time.sleep(3)
            print("Disconnection success!")
            return "success"
        except:
            print("Disconnection failed, wait for 5 seconds and try again...")
            time.sleep(5)
            Disconnect()
    else:
        print("Can't find the process!")
        return


def Check_for_Broadband():
    connections = []
    connections = win32ras.EnumConnections()
    if (len(connections) == 0):
        print("The system is not running any broadband connection.")
        return
    else:
        print("The system is running %d broadband connection." % len(connections))
        return connections


def ShowIpAddress(handle):
    print(win32ras.GetConnectStatus(handle))
    data = os.popen("ipconfig", "r").readlines()
    have_ppp = 0
    ip_str = None
    for line in data:
        if line.find("宽带连接") >= 0:
            have_ppp = 1
        # if your system language is English, you should write like this:
        # if have_ppp and line.strip().startswith("IP Address"):
        # in othewords, replace the "IPv4 地址" to "IP Address"
        if have_ppp and line.strip().startswith("IPv4 地址"):
            ip_str = line.split(":")[1].strip()
            have_ppp = 0
            print(ip_str)


# get my ipaddress anf disconnect broadband connection.
def re_connect():
    print('异常监测进程已启动,进程ID： ', os.getpid())
    while True:
        #进程监测抓取异常超过100次，则重新拨号更换IP
        if db.error_data.count({'error_count':'1'}) >= 100:
            data = Check_for_Broadband()
            if data != None:
                for p in data:
                    # ShowIpAddress(p[0])
                    if (Disconnect(p[0]) == "success"):
                        print("%s has been disconnected." % p[1])
                    time.sleep(5)

            pid, res = DialBroadband()
            time.sleep(5)
            # ShowIpAddress(pid)
            # time.sleep(5)
            # Disconnect(pid)
            db.error_data.drop()
            time.sleep(10)

# re_connect()



    # if exist running broadband connection, disconnected it.
    # if data != None:
    #     for p in data:
    #         ShowIpAddress(p[0])
    #         if (Disconnect(p[0]) == "success"):
    #             print("%s has been disconnected." % p[1])
    #         time.sleep(3)
    # else:
    #     pid, res = DialBroadband()
    #     ShowIpAddress(pid)
    #     time.sleep(3)
    #     Disconnect(pid)
    # return "finsh test"

#
# test = re_connect()
# print(test)
