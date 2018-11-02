#使用twstock第三方套件用來擷取股票資訊
import twstock

#使用Linebot必需相關套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('rz8fKvur7vNcnM0JFKWhQmYLbQ3S8bAqgPIrzMUemu8OSNWcnGOhQ2mwHPori/szTD8X95qpS51bCoYzubPWBL1DhH0RYMNdY5veolcTn6FSsOe0X8DtvByAmLDMiaL3ZTQlWZKGgzIdwQT5PLNdzwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6ecfeddf3c70fd59a0003caf60827bbf')

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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #擷取當前輸入正確代碼股票twstock套件中的realtime資訊
    stockdata = twstock.realtime.get(event.message.text)
    #擷取realtime資訊中的股票"資訊""名稱"及"即時""股價"
    nowValue = stockdata['info']['name']+('\n')+stockdata['realtime']['latest_trade_price']
    addtionalMsg = 'How are you'
    #傳回Line平台
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=nowValue + addtionalMsg))

 
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
