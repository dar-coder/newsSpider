from flask import Flask, render_template
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import requests
import ssl

app = Flask(__name__)

@app.route('/')
def index():
	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	

	# Retreiving and parsing the html for the World News section
	# (scraping CNN's website)
	html_world = urllib.request.urlopen('https://edition.cnn.com/world', context=ctx).read()
	soup = BeautifulSoup(html_world, 'html.parser')

	# All the news for the World News section will be stored in a 'world dictionary'
	# This dictionary will have 5 key-value pairs:
	# The keys will be the 5 continents and each of the vaules will be a dictionary containing the news headline and the link
	world = {}

	# Scraping CNN's website for the top Europe news and storing the result in the 'world dictionary'
	tag_europe = soup.find('h3', {'data-analytics': 'Europe_list-hierarchical-xs_article_'})
	tag_europe_text = tag_europe.find('span', {'class': 'cd__headline-text'}).text
	tag_europe_link = 'https://edition.cnn.com' + tag_europe.find('a').get('href', None)
	world['Europe'] = {tag_europe_text: tag_europe_link}

	# Scraping CNN's website for the top Middle East news and storing the result in the 'world dictionary'
	tag_middle_east = soup.find('h3', {'data-analytics': 'Middle East_list-hierarchical-xs_article_'})
	tag_middle_east_text = tag_middle_east.find('span', {'class': 'cd__headline-text'}).text
	tag_middle_east_link = 'https://edition.cnn.com' + tag_middle_east.find('a').get('href', None)
	world['Middle East'] = {tag_middle_east_text: tag_middle_east_link}

	# Scraping CNN's website for the top Africa news and storing the result in the 'world dictionary'
	tag_africa = soup.find('h3', {'data-analytics': 'Africa_list-hierarchical-xs_article_'})
	tag_africa_text = tag_africa.find('span', {'class': 'cd__headline-text'}).text
	tag_africa_link = 'https://edition.cnn.com' + tag_africa.find('a').get('href', None)
	world['Africa'] = {tag_africa_text: tag_africa_link}

	# Scraping CNN's website for the top Americas news and storing the result in the 'world dictionary'
	tag_americas = soup.find('h3', {'data-analytics': 'Americas_list-hierarchical-xs_article_'})
	tag_americas_text = tag_americas.find('span', {'class': 'cd__headline-text'}).text
	tag_americas_link = 'https://edition.cnn.com' + tag_americas.find('a').get('href', None)
	world['Americas'] = {tag_americas_text: tag_americas_link}

	# Scraping CNN's website for the top Asia news and storing the result in the 'world dictionary'
	tag_asia = soup.find('h3', {'data-analytics': 'Asia _list-hierarchical-xs_article_'})
	tag_asia_text = tag_asia.find('span', {'class': 'cd__headline-text'}).text
	tag_asia_link = 'https://edition.cnn.com' + tag_asia.find('a').get('href', None)
	world['Asia'] = {tag_asia_text: tag_asia_link}


	

	# Retreiving and parsing the html for the Movies, TV and Celebrities News section
	# (scraping IMDB's website)
	html_movies = urllib.request.urlopen('https://www.imdb.com/news/movie?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b688335a-3266-4b15-ab7b-ab8edbc4b1c4&pf_rd_r=4S4C27BHSEX6Y40GDYJT&pf_rd_s=center-6&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_nw_mv_tb', context=ctx).read()
	soup_movies = BeautifulSoup(html_movies, 'html.parser')

	# All the news for the Movies, TV and Celebrities News section will be stored in a 'movie' dictionary
	# This dictionary will have 5 key-value pairs:
	# The keys will be the 5 top news title and each of the vaules will be the respective link
	movies = {}

	tag_movies_div = soup_movies.find('div', {'class': 'aux-content-widget-4 news-sidebar-widget'})
	tag_movies_anchor = tag_movies_div.findChildren('a', {'class': 'compact-news-item__title'})

	for anchor in tag_movies_anchor:
		movies[anchor.text] = 'https://www.imdb.com' + anchor.get('href', None)


	

	# Retreiving and parsing the html for the Sports News section
	# (scraping skysports' website)
	html_sports = urllib.request.urlopen('https://www.skysports.com', context=ctx).read()
	soup_sports = BeautifulSoup(html_sports, 'html.parser')

	# All the news for the Sports News section will be stored in a 'sports' dictionary
	# This dictionary will have 5 key-value pairs:
	# The keys will be the 5 latest news titles and each of the vaules will be the respective link
	sports = {}

	tag_sports_div = soup_sports.find('div', {'class': 'sdc-site-tiles__group'})
	tag_sports_titles = tag_sports_div.findChildren('h3', {'class': 'sdc-site-tile__headline'})

	# We've scraped more than 5 latest news articles, and we need only the first 5
	for i in range(5):
		text = tag_sports_titles[i].find('span', {'class': 'sdc-site-tile__headline-text'}).text
		link = tag_sports_titles[i].find('a').get('href', None)
		if not 'skysports.com' in link:
			link = 'https://www.skysports.com' + link
		sports[text] = link


	

	# Retreiving and parsing the html for the Science News section
	# (scraping sciencedaily's website)
	# This website blocks spiders/bots, so there's a 'User-Agent' passed in the request as a header in order to 
	# bypass the site's security
	req = urllib.request.Request('https://www.sciencedaily.com/news/', headers={'User-Agent': 'Mozilla/5.0'})
	html_science = urllib.request.urlopen(req, context=ctx).read()
	soup_science = BeautifulSoup(html_science, 'html.parser')

	# All the news for the Science News section will be stored in a 'science' dictionary
	# This dictionary will have 5 key-value pairs:
	# The keys will be the 5 latest news titles and each of the vaules will be the respective link
	science = {}

	tag_science = soup_science.find('ul', {'id': 'featured_shorts'})
	tag_science_titles = tag_science.findChildren('li')

	# We've scraped more than 5 latest news articles, and we need only the first 5
	for i in range(5):
		text = tag_science_titles[i].text
		link = 'https://www.sciencedaily.com' + tag_science_titles[i].find('a').get('href', None)
		science[text] = link

	



	return render_template('index.html', world=world, movies=movies, sports=sports, science=science)