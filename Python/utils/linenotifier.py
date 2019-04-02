# Follow the command below to install LINE SDK and Google-Cloud-Storage
# $> pip install line-bot-sdk
# $> pip install google-cloud-storage
#
from threading import Thread
from linebot import LineBotApi
from linebot.models import (TextSendMessage, ImageSendMessage)
from linebot.exceptions import LineBotApiError
from google.cloud import storage
import os

class LINENotifier:
	def __init__(self, conf):
		# store the configuration object
		self.conf = conf

	def sendPush(self, msg, dest, type):
		t = Thread(target=self._sendPush, args=(msg, dest, type))
		t.start()

	def _sendPush(self, msg, dest, type):
		channel_access_token = self.conf.CHANNEL_ACCESS_TOKEN
		line_bot_api = LineBotApi(channel_access_token)

		if type == "TXT":
			try:
				line_bot_api.push_message(dest, TextSendMessage(text=msg))

			except LineBotApiError as e:
				# error handle
				print(e.status_code)
				print(e.error.message)
				print(e.error.details)
		elif type == "IMG":
			bucket_id = self.conf.BUCKET_ID
			bucket_dir = self.conf.BUCKET_DIR
			remote_path = bucket_dir + os.path.basename(msg)
			local_path = msg
			print(remote_path)

			# Create a Google Storage Client object
			client = storage.Client.from_service_account_json(
				self.conf.GOOGLE_APPLICATION_CREDENTIALS)

			bucket = client.get_bucket(bucket_id)

			# upload the file
			blob = bucket.blob(remote_path)
			blob.upload_from_filename(filename=local_path)
			blob.make_public()

			# DEBUG: Check the result
			#print("Blob {} is publicly accessible at {}".format(
			#	blob.name, blob.public_url))

			# Send to LINE API Server
			try:
				line_bot_api.push_message(dest, ImageSendMessage(
					original_content_url=blob.public_url,
					preview_image_url=blob.public_url))

			except LineBotApiError as e:
				# error handle
				print(e.status_code)
				print(e.error.message)
				print(e.error.details)

