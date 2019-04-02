from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

ChannelAccessToken = "ChannelAccessToken"
ToUid = "Ua683d0cd676d5b"

line_bot_api = LineBotApi(ChannelAccessToken)

try:
	line_bot_api.push_message(ToUid, TextSendMessage(text='Test message from Python Bot!'))

except LineBotApiError as e:
	# error handle
	print(e.status_code)
	print(e.error.message)
	print(e.error.details)
