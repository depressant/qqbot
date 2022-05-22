import qqbot
import pandas as pd
import numpy as np


def _message_handler(event, message: qqbot.Message):
    msg_api = qqbot.MessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
    content = extract_message(message)
    global choice
    if choice == 1:
        jielong(event, message)
    elif choice == 2:
        daka(event, message)
    elif choice == 3:
        game_xiehouyu(event, message)
    else:
        if content == "成语接龙":
            choice = 1
            jielong(event, message)
        elif content == "打卡":
            choice = 2
            daka(event, message)
        elif content == "歇后语":
            choice = 3
            game_xiehouyu(event, message)
        else:
            send = qqbot.MessageSendRequest("<@%s> 请艾特我说【成语接龙】、【打卡】或者【歇后语】吧！" % message.author.id, message.id)
            msg_api.post_message(message.channel_id, send)
    # 构造消息发送请求数据对象
    # send = qqbot.MessageSendRequest("<@%s>谢谢你，加油!!!!" % message.author.id, message.id)
    # 通过api发送回复消息
    # msg_api.post_message(message.channel_id, send)


def jielong(event, message: qqbot.Message):
    msg_api = qqbot.MessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)
    qqbot.logger.info("event %s" % event + ",receive message %s" % message.timestamp)
    global score
    global last_weipin
    global flag
    global choice
    content = extract_message(message)
    if (content == "成语接龙" and flag == False):
        word = np.random.choice(chengyu.index)
        send = qqbot.MessageSendRequest(
            "<@%s> 快开始你的挑战吧，如果想退出对我说“不玩了”，想查看分数对我说“分数”， 下面是你要接的成语" % message.author.id + "【%s】" % word, message.id)
        msg_api.post_message(message.channel_id, send)
        last_weipin = chengyu.loc[word, "weipin"]
        flag = True
    elif (content == "不玩了" and flag == True):
        send = qqbot.MessageSendRequest("<@%s> 成功退出，你的得分为" % message.author.id + "【%s】" % score, message.id)
        score = 0
        flag = False
        choice = 0
        msg_api.post_message(message.channel_id, send)
    elif (content == "分数" and flag == True):
        send = qqbot.MessageSendRequest("<@%s> 你的得分为" % message.author.id + "【%s】" % score, message.id)
        msg_api.post_message(message.channel_id, send)
    elif (flag == True and content not in chengyu.index):
        send = qqbot.MessageSendRequest("<@%s> 你输入的不是一个成语，请重新输入" % message.author.id, message.id)
        msg_api.post_message(message.channel_id, send)
    elif (flag == True and chengyu.loc[content, "shoupin"] != last_weipin):
        send = qqbot.MessageSendRequest("<@%s> 请仔细观看上一个成语的结尾，再尝试一次吧" % message.author.id, message.id)
        msg_api.post_message(message.channel_id, send)
    elif (flag == True):
        words = chengyu.index[chengyu.shoupin == chengyu.loc[content, "weipin"]]
        word2 = np.random.choice(words)
        score += 1
        send = qqbot.MessageSendRequest("<@%s> 很厉害，你接对了，给你加一分，请接下一个成语 " % message.author.id + "【%s】" % word2,
                                        message.id)
        msg_api.post_message(message.channel_id, send)
        last_weipin = chengyu.loc[word2, "weipin"]
    elif (flag == False):
        send = qqbot.MessageSendRequest("<@%s> 请艾特我说成语接龙吧！" % message.author.id, message.id)
        msg_api.post_message(message.channel_id, send)


def daka(event, message: qqbot.Message):
    msg_api = qqbot.MessageAPI(t_token, False)
    global daka_count
    global daka_timeset
    global choice
    content = extract_message(message)
    time = message.timestamp[0:10]
    send = qqbot.MessageSendRequest("<@%s> 你今天已经打过卡了，明天再来吧" % message.author.id, message.id)
    if time not in daka_timeset:
        daka_count += 1
        send = qqbot.MessageSendRequest("<@%s> 恭喜你" % message.author.id + "%s打卡成功，累计打卡天数" % time + "%s" % daka_count,
                                        message.id)
    daka_timeset.add(time)
    choice = 0
    msg_api.post_message(message.channel_id, send)


def game_xiehouyu(event, message: qqbot.Message):
    msg_api = qqbot.MessageAPI(t_token, False)
    content = extract_message(message)
    global score_xiehouyu
    global flag
    global choice
    global xiehouyu
    send = 1
    global answer
    global answer_list
    global answer_count
    if flag == False:
        question = np.random.choice(xiehouyu.index)
        answer = xiehouyu.loc[question, "answer"]
        print(answer)
        answer_list.clear()
        answer_list.append(answer)
        pos = answer.find("；")
        if pos != -1:
            answer_list = answer.split("；")
            answer_count = len(answer_list)
        flag = True
        send = qqbot.MessageSendRequest(
            "<@%s> 快来开始你的挑战吧！如果想退出请对我说“不玩了”，下面是为你准备的歇后语谜面：" % message.author.id + "%s" % question, message.id)
    else:
        if content == "不玩了":
            send = qqbot.MessageSendRequest("<@%s> 成功退出，你的得分为" % message.author.id + "【%s】" % score_xiehouyu,
                                            message.id)
            score_xiehouyu = 0
            flag = False
            choice = 0
        elif content == "分数":
            send = qqbot.MessageSendRequest("<@%s> 你目前的得分为" % message.author.id + "【%s】" % score_xiehouyu,
                                            message.id)
        elif content == "答案":
            question = np.random.choice(xiehouyu.index)
            send = qqbot.MessageSendRequest(
                "<@%s> 实在猜不出来了吧，告诉你答案吧，答案是" % message.author.id + "【%s】" % answer + " 快来接下一个歇后语吧%s" % question,
                message.id)
            answer = xiehouyu.loc[question, "answer"]
            answer_list = answer
            pos = answer.find("；")
            if pos != -1:
                answer_list = answer.split("；")
                answer_count = len(answer_list)
        else:
            send = qqbot.MessageSendRequest("<@%s> 不对哦，再猜猜吧，想知道答案可以对我说“答案”" % message.author.id, message.id)
            for res in answer_list:
                if content == res:
                    score_xiehouyu += 1
                    question = np.random.choice(xiehouyu.index)
                    send = qqbot.MessageSendRequest(
                        "<@%s> 恭喜你答对了，再加一分，你目前分数为" % message.author.id + "【%s】" % score_xiehouyu + "快来接受下一次挑战吧%s" % question,
                        message.id)
                    answer = xiehouyu.loc[question, "answer"]
                    answer_list = answer
                    pos = answer.find("；")
                    if pos != -1:
                        answer_list = answer.split("；")
                        answer_count = len(answer_list)
                    break
    msg_api.post_message(message.channel_id, send)


def extract_message(message: qqbot.Message):
    pos = message.content.find(">")
    content = message.content[pos + 1:len(message.content)]
    content = content.strip()
    return content


def main():
    # 注册事件类型和回调，可以注册多个
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    qqbot.listen_events(t_token, False, qqbot_handler)


# t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
# # 注册事件类型和回调，可以注册多个
# qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
# qqbot.listen_events(t_token, False, qqbot_handler)
if __name__ == '__main__':
    chengyu = pd.read_json("utils/chinese-xinhua/data/idiom.json")
    t = chengyu.pinyin.str.split()
    chengyu["shoupin"] = t.str[0]
    chengyu["weipin"] = t.str[-1]
    chengyu = chengyu.set_index("word")[["shoupin", "weipin"]]
    last_weipin = 1

    xiehouyu = pd.read_json("utils/chinese-xinhua/data/xiehouyu.json")
    t1 = xiehouyu.answer
    xiehouyu["answer"] = t1
    xiehouyu = xiehouyu.set_index("riddle")[["answer"]]
    xiehouyu_last = 0
    score_xiehouyu = 0
    answer = 0
    answer_list = list()
    answer_count = 1

    score = 0
    flag = False
    choice = 0
    daka_count = 0
    daka_timeset = set()
    token = qqbot.Token("*****", "*******")
    api = qqbot.UserAPI(token, False)
    user = api.me()
    t_token = token
    main()
