# 主要用來接收使用者訊息


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    TextMessage,ImageMessage,VideoMessage,AudioMessage,LocationMessage,StickerMessage,FileMessage,
    StickerSendMessage,TextSendMessage,TemplateSendMessage,FlexSendMessage,ImageSendMessage
)

        
app = Flask(__name__)

# my token
line_bot_api = LineBotApi(
    'FZT/Idi+V+pcZxmnRfOOKYOzn3nlG6RG9Ohiiys5dqzc03Mqh3f8X/CEfrRzje9uUiy3SaBMVFXe+ua8jusQULhNucGkcKxBxEfVIKSui40Je9L0LVVTwP4sPTYBPvuHCXatUfjO1OXxBflsdXDxUQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b55f6ebc8596d8df0b139f4991851fa7')


@app.route("/")
def home():
    # if success
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


def replyText_func(user_msg):
    global replyText
    
    replyText = '嗷嗷嗷嗷嗷嗷嗷嗷嗷嗷嗷'

    if '安安' in user_msg:
        replyText = '安甚麼安'
    if '胖' in user_msg:
        replyText = '你最胖'
    if '令謙' in user_msg:
        replyText = '老人家'
    print(replyText)
    return replyText



# 處理訊息
@handler.default()
def default(event):
    global replyText
    
    # 使用者id
    sender_id = event.source.user_id
    # 判別訊息類型
    msgType = event.message.type
    
    if msgType == 'text':
        # 回復使用者訊息
        user_msg = event.message.text
        replyText_func(user_msg)
        reply = TextSendMessage(text=replyText)
        line_bot_api.reply_message(event.reply_token,reply)
    elif msgType == 'sticker':
        sticker_message = StickerSendMessage(
            package_id='6359',
            sticker_id='11069865'
        )
        line_bot_api.reply_message(event.reply_token,sticker_message)
        line_bot_api.push_message(sender_id,TextSendMessage(text='你傳貼圖吼'))
    else:
        replyText = '有好康的直接傳給peco(✪ω✪)'
        reply = TextSendMessage(text=replyText)
        line_bot_api.reply_message(event.reply_token,reply)
    
if __name__ == "__main__":
    app.run()
