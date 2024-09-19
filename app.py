import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SourceUser,SourceGroup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Get sensitive information from environment variables
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/")
def home():
    return "Welcome to My Line Chat Bot! \n เขียนให้ดูรกๆ \n รกๆอีกสักบรรทัด >>*<< \n (Kanpot: Demo LineChatBot)"

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
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="วันนี้น้อนโส้มจะทำไอเอฟก๊าบ"))

    elif text == "ไออ้วน":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ไออ้วนไม่กินปลา"))

    elif text == "อยากผอมจัง":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ออกกำลังกายมั้ยจ้า หรือ ทำ IF ดีน๊า"))

    elif text == "พี่ส้ม":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="อาทิตย์นี้พี่ส้มกินชาเย็นเกิน2แก้วแล้วยังน๊าา"))

    elif text == "ฮึ้บ":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ฮึ้บๆน้าค้าบ เป็นกำลังใจให้จ๊าา"))       


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

if __name__ == "__main__":
    app.run(port=10000)