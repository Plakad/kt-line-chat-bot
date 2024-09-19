import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SourceUser

app = Flask(__name__)

line_bot_api = LineBotApi("UOSxZp9mU5bdu0XhuStH2vsg9rRdS0FxUbAOg+7eyjWc7OUTt68D996qsH1H5CtkhnlJkpGAMjAnDzbYnMfA8p14OVMDnOeEDTCus/r7umTfLGXCIaqxA8/7PTZs/mXHhUJGfSWHLsIl4OGUo5C1rgdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("702054376e553a49abd154de87dd8821")

@app.route("/")
def home():
    return "Welcome to My Line Chat Bot! \n เขียนให้ดูรกๆ \n (Kanpot: Demo LineChatBot)"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Reply with the same message that the user sent
    text = event.message.text
    if text == "น้อนโส้ม":
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="วันนี้น้อนโส้มจะทำไอเอฟก๊าบ"))

    elif text == "ไออ้วน":
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ไออ้วนไม่กินปลา"))

    elif text == "อยากผอมจัง":
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ออกกำลังกายมั้ยจ้า หรือ ทำ IF ดีน๊า"))        


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

if __name__ == "__main__":
    app.run(port=10000)