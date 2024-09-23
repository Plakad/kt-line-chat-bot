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
    return "Welcome to My Line Chat Bot! \n'\ เขียนให้ดูรกๆ \n'\ รกๆอีกสักบรรทัด >>*<< \n'\ (Kanpot: Demo LineChatBot)"

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
        app.logger.error("Invalid signature. Check your channel access token/secret.")
        abort(400)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        abort(500)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Reply with the same message that the user sent
    text = event.message.text

    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    display_name = profile.display_name
    if text == str("123"):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"123 ทดสอบ ทดสอบ !!!"))

    elif text == "กินอะไรดี":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"กะเพราหรือกินเตี๋ยวดีครับ"))

    elif text == "กะเพรา":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"เอาไข่ดาวด้วยมั้ย"))

    elif text == "กินเตี๋ยว":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ก็ดีน้า เบาๆดี"))

    elif text == "ฮึ้บ":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ฮึ้บๆน้าค้าบ เป็นกำลังใจให้จ๊าา"))

    elif text == "อย่างสีเหลือง":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="เยลลี่? /nเอ้ย เยลโล่"))      

    # elif text == str("555"):
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ตาหลกแล๊ะ!!"))

    # elif text == "เทอ":
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ว่าไงจ๊าาา"))  

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text))


if __name__ == "__main__":
    app.run(port=10000)