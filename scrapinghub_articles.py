"""Module for getting a list of articles published on ScrapingHubs blog.

Script will iterate through each page on the blog list and save the title
and url for each article. It will then format each article into a markdown
file that can be used to quickly read through all the titles.
"""
import requests
from datetime import datetime
from bs4 import BeautifulSoup


articles = []
page = 0

while True:
    page += 1
    url = f"https://blog.scrapinghub.com/page/{page}"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for post in soup.find_all('div', class_='post-item'):
        link = post.select_one('h2 a')
        date = post.select_one('span.date').text.strip()

        articles.append({
            'title': link.text, 
            'url': link['href'], 
            'date': datetime.strptime(date, '%B %d, %Y'),
        })

    if soup.find('a', class_='next-posts-link') is None:
        break

with open('scrapinghub_articles.md', 'w') as f:
    f.write("# Scraping Hub Articles\n\n")
    for article in articles:
        if article['title'] and article['url']:
            f.write(f"* {article['date'].strftime('%Y-%m-%d')} [{article['title']}]({article['url']})\n")
