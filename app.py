import os
from flask import Flask, request, abort,  jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SourceUser,SourceGroup
from dotenv import load_dotenv
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Get sensitive information from environment variables
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/")
def home():
    return "Welcome to My Line Chat Bot! \n'\ เขียนให้ดูรกๆ \n'\ รกๆอีกสักบรรทัด >>*<< \n'\ (Kanpot: Demo LineChatBot)"

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        # Optionally log the GET request or just return a simple response
        logging.info("GET request received. Returning OK.")
        return 'OK', 200

    # Handle POST requests as normal
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    if signature:
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            logging.error("Invalid signature")
            abort(400)
        return 'OK'

    if not body:
        logging.info("Empty POST request received.")
        return jsonify({"error": "Empty POST request"}), 400

    return 'OK', 200

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
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="เยลลี่? \nเอ้ย เยลโล่"))      

    elif text == str("555"):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ตาหลกแล๊ะ!!"))

    elif text == "wake up":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ตื่งแล้วจ้าา")) 

    elif text == "อย่างสีเหลือง":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="เยลลี่? \nเอ้ย เยลโล่"))      

    elif text == str("555"):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"ตาหลกแล๊ะ!!"))

    elif text == "ป้าส้ม":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="วันนี้ป้าส้มจะ IF แล้วนะ!!!\nจริงๆนะ"))      


    elif text == "พี่ส้ม":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"อยากกินชาเย็นกับเอสเย็นทุกวันเลยโว้ยย")) 

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text))


if __name__ == "__main__":
    app.run(port=10000)