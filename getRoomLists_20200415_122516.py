#coding=utf8
'''
import itchat
import time

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register('Text')
def text_reply(msg):
    # 当消息是‘退出’的时候
    if msg['Text'] == '退出':
        itchat.logout()
        return null
    
    else: # not msg['FromUserName'] == myUserName:
        # 发送一条提示给文件助手
        #itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
        itchat.send_msg(u"[%s]收到：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg), 'filehelper')
        # 回复给好友
        #return u'[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的的信息：%s\n' % (msg['Text'])
        return u'[自动回复]%s\n' % (msg['Text'])
'''

import itchat, time
from itchat.content import *
import os
import sys
import xlwt
import itchat,time
import re

last_msg = None

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    last_msg = msg
    msg.user.send('您好，我现在有事不在，一会再和您联系')#('%s: %s' % (msg.type, msg.text)).replace('任茂林','茂林').replace('茂林',msg.actualNickName))

'''
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        msg.user.send(msg.text.replace('\@任茂林','\@%s' % (msg.actualNickName).replace('茂林',msg.actualNickName))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

#@itchat.msg_register(FRIENDS)
#def add_friend(msg):
    #msg.user.verify()
    #msg.user.send('Nice to meet you!')
'''
def correctChars(name):
    return re.subn(r'(^|[^0-9])0?([1-3]|一|二|三)[层楼層樓一—～-]',r'\1\2层',\
                   name.replace('二区','').replace('02区','').replace('2区',''))[0]\
                   .replace('一层','1层').replace('二层','2层').replace('三层','3层')\
                   .replace('一楼','1层').replace('二楼','2层').replace('三楼','3层')\
                   .replace('O','0').replace('o','0')\
                   .replace(' ','').replace('，',',').replace('*',',').replace('、',',').replace('.',',').replace('一','-')\
                   .replace('\'',',').replace('Ｂ','B').replace('--','')\
                   .replace('层3-','层3').replace('商1','1').replace('商2','2').replace('商3','3').upper()\
                   .replace('3B','2层3B').replace('2层2层','2层').replace(r'3A-',r'3A').replace(r'3B-',r'3B').replace('A(\d{3})',r'3A\1').replace('33A','3A')

def formatname(name):
    if len(name) < 1 :
        return name
    return correctChars(name)
    

def get_chatroom_users(qunname, workbook):
    try:
        #根据群聊名称在表单中创建工作薄
        worksheet=workbook.add_sheet(qunname, cell_overwrite_ok=True) #.add_worksheet(roomslist[i]['NickName'])
        #添加表头
        worksheet.write(0,0,"微信名称")
        worksheet.write(0,1,"群备注")
        #获取群聊用户列表
        myroom=itchat.search_chatrooms(name=qunname)
        #获取群聊名称
        gsp=itchat.update_chatroom(myroom[0]['UserName'], detailedMember=True)
        print("\n群名：{} \t 人数：{}".format(qunname,len(gsp['MemberList'])))

        nickname=[]
        displayname=[]

        for c in gsp['MemberList']:
            nickname.append(c['NickName'])
            displayname.append(c['DisplayName'])

        msg = '请以下业主修改群昵称为"2层3B123姓名"或"2层3A123姓名"格式，不会修改的请亲友或者群友帮忙:\r\n'
        #将用户信息写入相应的工作薄中
        for x in range(len(gsp['MemberList'])):
            worksheet.write(x+1,0,nickname[x])
            worksheet.write(x+1,1,displayname[x])
            fn = formatname(displayname[x])
            worksheet.write(x+1,2,fn)
            if len(fn) < 1:
                fn = nickname[x]
            mm = re.search('3[AB]-*\d{2,3}',fn)
            if mm == None:
                if not fn in ['英','朱勇','顺其自然']:
                    msg += '@%s '%fn
                    #print('@%s'%fn)
            else:
                worksheet.write(x+1,3,mm.group(0))
        print(msg)
        itchat.send_msg(msg, toUserName=myroom[0]['UserName'])
          
        #输出一点提示信息
        print('\n结束.')#,end='')#            "sheet {} finished".format(roomslist[i]['NickName']))
        
    except Exception as e:
        print("Error",e)
        
def get_one_chatroom_users(qunname):
    workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)

    get_chatroom_users(qunname,workbook)
        
    #关闭工作表
    workbook.save(qunname+".xls")
    
def get_all_chatroom_user_list():
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    # @Date    : 2019-08-22 17:30:40
    # @Author  : WangGuo
    # @GitHub  : https://github.com/King-Key
    # @Blog    : https://blog.csdn.net/King_key
    # @Website　: https://king-key.github.io
    # @Email   : guo_wang_113@163.com


     #其中hotReload=True参数是为了短暂记忆登录状态，避免每登录一次就扫一次二维码
    #itchat.auto_login(hotReload=True)
    
    #获取群聊信息
    roomslist = itchat.get_chatrooms(update=True)

    #插入excel
    #创建excel表单
    #workbook=xlsxwriter.Workbook("群聊用户名单.xlsx")
    
    #创建一个Workbook对象，相当于创建了一个Excel文件
    workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)

    for i in range(0,len(roomslist)-1):
        qunname = roomslist[i]['NickName']
        get_chatroom_users(qunname,workbook)
        
    #关闭工作表
    workbook.save("list.xls")#.close()


if __name__ == '__main__':
    #itchat.auto_login()
    itchat.auto_login(hotReload=True)

    get_one_chatroom_users('湾畔商铺二层业主之家')
    #get_one_chatroom_users('湾畔二层3B业主之家')
    #get_all_chatroom_user_list()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    
    #itchat.run()
