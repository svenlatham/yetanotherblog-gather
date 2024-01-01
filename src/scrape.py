import requests
from bs4 import BeautifulSoup
import html2text
import os

def fetch_urls(base_url):
    # Fetch the list of URLs for all posts
    urls = []
    page = 1
    while True:
        response = requests.get(f"{base_url}/page/{page}/")
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        if not articles:
            break
        for article in articles:
            link = article.find('a', href=True)
            if link:
                urls.append(link['href'])
        page += 1
    return urls

def scrape_to_md(url, output_dir):
    response = requests.get(url)
    print(f"Scraping {url}")
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').get_text()  # Adjust selector based on your site's structure
    content = soup.find('div', {'class': 'post-content'})  # Adjust selector

    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown_content = h.handle(str(content))

    # Ensure that the title is safe for windows file structures:
    # https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
    title = title.replace('\\', '_')
    title = title.replace('/', '_')
    title = title.replace(':', '_')
    title = title.replace('*', '_')
    title = title.replace('?', '_')
    title = title.replace('"', '_')
    title = title.replace('<', '_')
    title = title.replace('>', '_')
    title = title.replace('|', '_')


    file_name = f"{output_dir}/{title.replace(' ', '_')}.md"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    base_url = 'https://www.yetanotherblog.com'  # Replace with your website
    output_dir = '/output'
    os.makedirs(output_dir, exist_ok=True)

    post_urls = fetch_urls(base_url)
    for post_url in post_urls:
        scrape_to_md(post_url, output_dir)
