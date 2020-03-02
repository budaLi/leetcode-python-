# @Time    : 2020/3/2 14:19
# @Author  : Libuda
# @FileName: outlook.py
# @Software: PyCharm
import re
from win32com.client.gencache import EnsureDispatch as Dispatch
import pandas as pd


def read_email(date, my_account, sent_account):
    # 读取邮箱
    outlook = Dispatch("Outlook.Application")
    mapi = outlook.GetNamespace("MAPI")
    Accounts = mapi.Folders

    # 读取的员工账号
    names = []
    # 短信内容
    contents = []
    # 读取邮件存入pandas
    c = ['Root_Directory_Name_1', 'Level_1_FolderName_1', 'Level_2_FolderName_1', 'ReceivedTime_1', 'SenderName_1',
         'to_to_1', 'cc_cc_1', 'Subject_1', 'MessageID_1', 'ConversationTopic_1', 'ConversationID_1',
         'ConversationIndex_1', 'EmailBody_1']
    df = pd.DataFrame(columns=c)

    for Account_Name in Accounts:
        # 只查找需要的邮箱账号信息

        if Account_Name.Name == my_account:
            print(' >> 正在查询的帐户名称：', Account_Name.Name, '\n')
            Level_1_Names = Account_Name.Folders
            for Level_1_Name in Level_1_Names:
                #             只需要收件箱的邮件
                if Level_1_Name.Name == '收件箱':
                    print(' - 正在查询一级目录：', Level_1_Name.Name)
                    Mail_1_Messages = Level_1_Name.Items
                    #                 将邮件按日期排序，可减少遍历内容
                    Mail_1_Messages.Sort("[ReceivedTime]", True)

                    for xx in Mail_1_Messages:  # xx = 'mail'  # 开始查看单个邮件的信息
                        print(xx.Subject)
                        Root_Directory_Name_1 = Account_Name.Name
                        Level_1_FolderName_1 = Level_1_Name.Name
                        Level_2_FolderName_1 = ''
                        ReceivedTime_1 = str(xx.ReceivedTime)[:10]  # 接收日期

                        if ReceivedTime_1 != date:  # 只要特定日期的邮件
                            continue

                        SenderName_1 = xx.SenderName  # 发件人

                        if SenderName_1 != sent_account:  # 只要特定发件人的邮件
                            continue

                        Subject_1 = xx.Subject  # 主题
                        EmailBody_1 = xx.Body  # 邮件内容
                        to_to_1 = xx.To  # 收件人
                        cc_cc_1 = xx.CC  # 抄送人
                        MessageID_1 = xx.EntryID  # 邮件MessageID
                        ConversationTopic_1 = xx.ConversationTopic  # 会话主题
                        ConversationID_1 = xx.ConversationID  # 会话ID
                        ConversationIndex_1 = xx.ConversationIndex  # 会话记录相对位置

                        data = [Root_Directory_Name_1, Level_1_FolderName_1, Level_2_FolderName_1, ReceivedTime_1,
                                SenderName_1, to_to_1, cc_cc_1, Subject_1, MessageID_1, ConversationTopic_1,
                                ConversationID_1, ConversationIndex_1, EmailBody_1]

                        dataf = dict(zip(c, data))
                        df = df.append(dataf, ignore_index=True)

    return df


while 1:
    import time

    time.sleep(10)
    res = read_email("2020-03-02", "15735656005@163.com", "1364826576@qq.com")
