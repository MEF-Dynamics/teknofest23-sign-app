from Constants import RUN_TEMP_FOLDER_PATH, connect_pathes
from googletrans import Translator
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import os

def translate_text(source_language:str, target_language:str, text:str) -> str:
	"""
	Method, to translate text from source language to target language.
	@Params:
		source_language: str - (Required) Source language of the text.
		target_language: str - (Required) Target language of the text.
		text: str - (Required) Text to be translated.
	@Returns:
		translation: str - Translated text.
	@Raises:
		Exception: If translation failed.
	"""

	translator = Translator()
	
	try :
		translation = translator.translate(text, src=source_language, dest=target_language)
		return translation.text
	except :
		raise Exception("Error: Translation failed, LOG: " + source_language + " " + target_language + " " + text)
	
def vocalize_text(vocalize_language:str, text:str) -> None:
	"""
	Method, to vocalize text in target language.
	@Params:
		vocalize_language: str - (Required) Target language of the text.
		text: str - (Required) Text to be vocalized.
	@Returns:
		None
	@Raises:
		Exception: If vocalization failed.
	"""

	try :
		speak = gTTS(text=text, lang=vocalize_language, slow=False)
	except :
		raise Exception("Error: Vocalization failed, LOG: " + text + " " + vocalize_language)
	
	f_path = connect_pathes(RUN_TEMP_FOLDER_PATH, "captured_voice.mp3")
	speak.save(f_path)
	speak = None
	playsound(f_path)
	os.remove(f_path)

def listen_text(listening_language:str, device_index:int=None) -> str:
	"""
	Method, to listen to text in target language.
	@Params:
		listening_language: str - (Required) Target language of the text.
		device_index: int - (Optional) Index of the device to listen to.
	@Returns:
		query: str - The text that was listened to.
	"""

	def _get_audio() -> str:
		"""
		Method, to get audio from the microphone.
		@Params:
			None
		@Returns:
			query: str - The text that was listened to.
		"""

		print("Listening ...")
		recognizer = sr.Recognizer()
		microphone = sr.Microphone(device_index=device_index)
		with microphone as source :
			recognizer.pause_threshold = 1
			#recognizer.adjust_for_ambient_noise(source) # -> open this when in a noisy environment
			audio = recognizer.listen(source)

		print("Recognizing ...")
		query = None
		try :
			query = recognizer.recognize_google(audio, language=listening_language)
		except Exception as e :
			print("Error: Couldn't understand, repeat that again please ..." + str(e))

		return query

	query = _get_audio()
	while query is None :
		query = _get_audio()

	return query