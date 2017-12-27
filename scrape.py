import timeit
from html.parser import HTMLParser
from urllib import request

#test app id: learn.kalilinux.tutorial

urls = [
	"https://play.google.com/store/apps/details?id=", # Google play's URL
]

class DataParsedException(Exception):
	def __init__(self, data):
		self.data = data

class Find(HTMLParser):
	flag = False

	def handle_starttag(self, tag, attrs):
		if tag == "span":
			for i in attrs:
				if i == ("itemprop", "genre"):
						self.flag = True

	def handle_data(self, data):
		# We raise an exception because it should take less time to
		# handle an interrupt than to continue parsing the page (untested but evidenced by stackoverflow)
		if self.flag:
			self.flag = False
			raise DataParsedException(data)

	def handle_endtag(self, tag):
		pass

html_parser = Find()

def return_category(application_id):
	for i in urls:
		try:
			html_data = request.urlopen(i + application_id)
		except request.HTTPError:
			# Must not be in this app store, try the next one
			continue
		except Exception as e:
			print(type(e))
			return "Failed connection to " + i

		try:
			html = str(html_data.read())
			html_parser.feed(html)
		except DataParsedException as e:
			html_parser.reset()
			return e.data
		except Exception as e:
			html_parser.reset()
			print(e)
			return "General error trying to get package " + str(application_id)
	return "Couldn't find app on any app store"

		
if __name__ == "__main__":
	from argparse import ArgumentParser

	parser = ArgumentParser(description="Get the category of an android application given the package name")
	parser.add_argument("packages", type=str, nargs='+', help="Package name")
	args = parser.parse_args()

	for i in args.packages:
		print(i, ":", return_category(i))
