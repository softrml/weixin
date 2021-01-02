#coding=utf8
import itchat
import sys
import re
import time

# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
from tuling import get_response

def exitScript():
    ''' 释放SystemExit异常，以便退出程序运行 '''
    print('Exit program.')
    raise SystemExit

debug = True
stop =False# True #
#@itchat.msg_register([])
#def others_reply(msg):
#    printMessage(msg)

@itchat.msg_register('Text')
def text_reply(msg):
    printMessage(msg)
    if u'作者' in msg['Text'] or u'主人' in msg['Text']:
        return u'你可以在这里了解他：https://github.com/littlecodersh'
    elif u'退出程序' == msg['Text'] or 'exit' == msg['Text']  :
        global stop
        stop = True
        #exitScript()
        return '已退出Itchat'
    elif msg['Text']=='debug':
        global debug
        debug = not debug
        return 'debug = '+str(debug)
    elif u'获取图片' == msg['Text']:
        itchat.send('@img@eve.jpg', msg['FromUserName']) # there should be a picture
    else:
        return '' #get_response(msg['Text']) or u'收到：' + msg['Text']
    
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    printMessage(msg)
    return ({ 'Picture': u'图片', 'Recording': u'录音',
        'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
        u'已下载到本地') # download function is: msg['Text'](msg['FileName'])

@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'], isFriendChat=True)
def mm_reply(msg):
    printMessage(msg)
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias']

@itchat.msg_register(['Text','Picture', 'Recording', 'Attachment','Sharing', 'Video'], isGroupChat = True)
def group_reply(msg):
    printMessage(msg)
    if msg['isAt']:
        return u'@%s\u2005%s' % (msg['ActualNickName'],
            get_response(msg['Text']) or u'收到：' + msg['Text'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'项目主页：github.com/littlecodersh/ItChat\n'
        + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
        + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])

##这个是用于监听是否有消息撤回
@itchat.msg_register('Note', isFriendChat=True, isGroupChat=True, isMpChat=True)
def information(msg):
    #这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)   #在返回的content查找撤回的消息的id
        old_msg = msg_information.get(old_msg_id)    #得到消息
        print(old_msg)
        if len(old_msg_id)<11:  #如果发送的是表情包
            itchat.send_file(face_bug,toUserName='filehelper')
        else:  #发送撤回的提示给文件助手
            msg_body = "告诉你一个秘密~" + "\n" \
                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "撤回了什么 ⇣" + "\n" \
                       + r"" + old_msg.get('msg_content')
            #如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

            # 将撤回消息发送到文件助手
            itchat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
            msg_information.pop(old_msg_id)
            
msg_information = {}
face_bug=None  #针对表情包的内容


@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing','Text','Picture', 'Recording', 'Attachment', 'Video'],isFriendChat=True, isGroupChat=True, isMpChat=True)
def handle_receive_msg(msg):
    global face_bug
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   #接受消息的时间
    msg_from = getFromName(msg)  #在好友列表中查询发送信息的好友昵称
    msg_time = msg['CreateTime']    #信息发送的时间
    msg_id = msg['MsgId']    #每条信息的id
    msg_content = None      #储存信息的内容
    msg_share_url = None    #储存分享的链接，比如分享的文章和音乐
    printMessage(msg)
    
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':     #如果发送的消息是文本或者好友推荐
        try:
            msg_content = msg['Text']
            print (msg_content)
        except:
            printMessageAll(msg)
        
    #如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']    #内容就是他们的文件名
        msg['Text'](str(msg_content))    #下载文件
        # print msg_content
    elif msg['Type'] == 'Card':    #如果消息是推荐的名片
        msg_content = msg['RecommendInfo']['NickName'] + '的名片'    #内容就是推荐人的昵称和性别
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += '性别为男'
        else:
            msg_content += '性别为女'

        print( msg_content)
    elif msg['Type'] == 'Map':    #如果消息为分享的位置信息
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()     #内容为详细的地址
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':     #如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']       #记录分享的url
        print (msg_share_url)
    face_bug=msg_content

##将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )
            
def getNickName(username):
    try:
        if username[1]=='@':
            return itchat.search_chatrooms(userName=username)['NickName']
        else:
            return itchat.search_friends(userName=username)['NickName']
    except:
        return username

def getFromName(msg):
    return getNickName(msg['FromUserName'])

def getToName(msg):
    return getNickName(msg['ToUserName'])

def printMessage(msg):
    print("\r\n")
    l = ['Type','Text','ActualNickName']
    try:
        print('From:',getFromName(msg),'=>To:',getToName(msg))
        for k in l:
            try:
                print(k,':',msg[k])
            except:
                pass
    except:
        print('***** error *****')
        if not debug:
            printMessageAll(msg)
    if debug:
        printMessageAll(msg)
        
def printMessageAll(msg):
    print('[Details:]')
    empties = []
    zeroes =[]
    for k, v in msg. items():
        if v == '':
            empties.append(k)
        elif v == 0:
            zeroes.append(k)            
        else:
            print(str(k)+":"+str(v))
    print("''：",empties)
    print("0：",zeroes)
    #print(msg)#['Type']+" "+msg['Text']+" ")
    
def getGroupList(群聊名称):
    itchat.dump_login_status() # 显示所有的群聊信息，默认是返回保存到通讯录中的群聊
    myroom=itchat.search_chatrooms(name=群聊名称) #群聊名称
    if myroom == None or len(myroom) ==0:
        print('没有找到群聊：'+群聊名称)
        return
    memberList = itchat.update_chatroom(myroom[0]['UserName'], detailedMember=True)
    #print(memberList['MemberList'])
    #获取群成员昵称和群昵称
    mlist = memberList['MemberList']
    for it in mlist: 
        print(it['NickName']+':'+it['DisplayName'])

def main():
    itchat.logout() #Reset the status
    itchat.auto_login(hotReload=True) #, enableCmdQR=True)
    print("Running....")
    #itchat.run() #失控，不好，用configured_reply()
    # 使用configured_reply方法
    global stop
    while not stop:
        itchat.configured_reply()
        # some other functions
        #time.sleep(1)

main()

