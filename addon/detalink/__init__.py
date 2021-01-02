import globalPluginHandler
import scriptHandler
import ui
import api
import textInfos
import re
import logHandler
import os.path
import subprocess
import sys
impPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(impPath)
import urllib.request
import HTMLParser
from NVDAObjects.UIA import UIA

htmlParser=HTMLParser.HTMLParser()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	vlcProc=None
	
	def getFocusedLink(self):
		obj=api.getFocusObject()
		if isinstance(obj, UIA):
			link=obj.name
		else:
			try:
				link=obj.value
			except:
				pass
		return link

	def getTitle(self, link):
		global htmlParser
		request=urllib.request.Request(link)
		request.add_header('user-agent', 'mozilla 5.10')
		#request.add_header("Range", "bytes=0-1024")
		html=urllib.request.urlopen(request).read().decode('utf-8')
		title=htmlParser.unescape(re.search('(?<=<title>).+?(?=</title>)', html, re.DOTALL).group().strip())
		
		return title 

	def script_linkTitle(self, gesture):
		link=self.getFocusedLink()
		self.vlcProc.terminate() if self.vlcProc is not None else None
		if link is None or link.startswith("http")==False:
			selection=api.getCaretObject().makeTextInfo(textInfos.POSITION_SELECTION).text
			if selection.startswith("http"):
				link=selection

			else:
				ui.message("Not a link.")
				
				return
		if(re.match(".*.(aac|mp4).*", link)):
			self.vlcProc=subprocess.Popen(["c:/program files/VideoLAN/vlc/vlc.exe","-Idummy", link])
			

		else:
			title=self.getTitle(link)
			ui.message(title)

	__gestures={
		"kb:NVDA+alt+q": "linkTitle"
	}