# limitations under the License

from bs4 import BeautifulSoup
import requests
import re

#We made these to lay out the websites we were going to use
"""
LINKS
1) CNBC
2) Business Insider
3) Motley Fool
4) Market Watch
5) Reuters
"""


link = ""

#Initialization of the user desired stock
ticker = ""
print("")
print("")

#Parses text from articles from various sources
def get_req_name(link):
	text = ""
	try:
		article = requests.get(link, timeout=5)
		page_content = BeautifulSoup(article.content, "lxml")
		for paragraph in page_content.find_all("p"):
			text += (paragraph.text)
	#This handles any errors related to connection timeouts and/or paywalls (e.g. WSJ)
	except requests.exceptions.ConnectionError:
		pass
	except requests.exceptions.ReadTimeoutError:
		pass
	except:
		pass
	return text

#Creates lists of news articles related to the stock from the source webpage
def analyze_sites(news_site):
	link = ""
	linklist = []
	if news_site == "CNBC":
		link = "https://www.cnbc.com/quotes/?symbol={}".format(ticker)
		article = requests.get(link, timeout=5)
		page_content = BeautifulSoup(article.content, "lxml")
		headlineDivs = page_content.find_all("div", class_ = "assets")
		for headline in headlineDivs:
			links = headline.find_all("a")
			for href in links:
				# Cuts out the "garbage" html links and wsj content, might be redundant
				if "https" in href['href'] and "wsj.com" not in href["href"]:
					linklist.append(href["href"])
		return(linklist)

	if news_site == "MW":
		link = "https://www.marketwatch.com/investing/stock/{}".format(ticker)
		article = requests.get(link, timeout=5)
		page_content = BeautifulSoup(article.content, "lxml")
		headlineHeaders = page_content.find_all("h3", class_ = "article__headline")
		for headline in headlineHeaders:
			links = headline.find_all("a")
			for href in links:
				if "https" in href['href'] and "wsj.com" not in href["href"]:
					linklist.append(href["href"])
		return(linklist)

	if news_site == "SA":
		link = "https://seekingalpha.com/symbol/{}".format(ticker)
		article = requests.get(link, timeout=5)
		page_content = BeautifulSoup(article.content, "lxml")
		headlineDivs = page_content.findAll("div", class_ = "symbol_article")
		for headline in headlineDivs:
			links = headline.find_all("a")
			for href in links:
				if "https" in href['href'] and "wsj.com" not in href["href"]:
					linklist.append("https://seekingalpha.com"+href["href"])
		return(linklist)



def run_quickstart():
	# [START language_quickstart]
	# Imports the Google Cloud client library
	# [START language_python_migration_imports]
	from google.cloud import language
	from google.cloud.language import enums
	from google.cloud.language import types
	# [END language_python_migration_imports]

	# Instantiates a client
	# [START language_python_migration_client]
	client = language.LanguageServiceClient()
	# [END language_python_migration_client]
	# The text to analyze

	#Getting the sources initialized so the algorithm can loop through it
	sources = ["CNBC", "MW", "SA"]
	sentimentSum = 0
	total_sites = 0
	for m in sources:
		sites = analyze_sites(m)
		total_sites += len(sites)
		for i in range(len(sites)):
			link = sites[i]
			text = get_req_name(link)
			document = types.Document(
				content=text,
				type=enums.Document.Type.PLAIN_TEXT)
    # hi
    # Detects the sentiment of the text
			#Catches more errors that occur during the actual sentiment analysis; these are rare but still good to have
			try:
				sentiment = client.analyze_sentiment(document=document).document_sentiment
				sentimentSum += sentiment.score * sentiment.magnitude
			except:
				pass
	#Returning the Average Sentiment Score [ ASS for short ;) ]
	return (sentimentSum / total_sites)

    # [END language_quickstart]

try:
	if __name__ == '__main__':
		print("")
		print("")
		print("Requested stock, {}, returned a sentiment value of ".format(ticker) + str(run_quickstart()) + "!")

except:
	print("Something went wrong!")
