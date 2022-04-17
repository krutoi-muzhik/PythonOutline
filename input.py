import requests
import time

def GetResponceText (url):
	responce = requests.get (url)
	time.sleep (5)
	text = responce.text
	return text

class ABOBA:
	def biba ():
		pass
	boba = 1

def main ():
	url = "https://google.com"
	print (GetResponceText (url))

if __name__ == "__main__":
	main ()