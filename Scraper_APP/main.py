import requests
from bs4 import BeautifulSoup
from taipy.gui import Gui, notify
from time import sleep

placeholder_image = ""

# Initialize empty variables
title1 = author1 = link1 = image1 = ""
title2 = author2 = link2 = image2 = ""
title3 = author3 = link3 = image3 = ""
title4 = author4 = link4 = image4 = ""
title5 = author5 = link5 = image5 = ""
title6 = author6 = link6 = image6 = ""
title7 = author7 = link7 = image7 = ""
title8 = author8 = link8 = image8 = ""
title9 = author9 = link9 = image9 = ""
title10 = author10 = link10 = image10 = ""



# Base URL
URL = "https://techcrunch.com/category/artificial-intelligence/"

def scrape_ai_news(state):
    while True:
        try:
            response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, "html.parser")
            
            articles = soup.find_all("li",{"class":"wp-block-post"})
            print(len(articles))
            i = 0
            max_articles = 10
            while i < len(articles) and i < max_articles:

                article = articles[i]
                
                # Image
                img_tag = article.find("img",{"class":"attachment-card-block-16x9"})
                image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else placeholder_image

                # Title
                title_tag = article.find("a",{"class":"loop-card__title-link"})
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                
                if title:
                    link = title_tag.get("href")
                # Summary/Paragraph
                author_tag = article.find("a", {"class":"loop-card__author"})
                author = author_tag.get_text(strip=True) if author_tag else "No author available."
            

                setattr(state, f"title{i+1}", title)
                setattr(state, f"link{i+1}", link)
                setattr(state, f"author{i+1}", author)
                setattr(state, f"image{i+1}", image)
                i += 1

            notify(state, "success", "AI News Scraped Successfully!")

        except Exception as e:
            notify(state, "error", f"Scraping failed: {e}")
        sleep(10)

# HTML content for GUI
page = """
<style>
/* General dark purple background */
.taipy-dark {
    background: linear-gradient(to bottom right, #2e2157, #3b2b8c);
    color: white;
}

/* Main content area with glass effect */
main {
    background: rgba(53, 58, 111, 0.6) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}

/* Center title and button */
h1, .taipy-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #e0d8ff;
    margin-bottom: 20px;
}

/* Button style */
button {
    display: block;
    margin: 0 auto 40px auto;
    background-color: #6c4acb;
    color: white;
    font-weight: bold;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
    background-color: #7e5de5;
    transform: scale(1.05);
}

/* Article title */
.title {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 5px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #e0d8ff;
    text-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

/* Author info */
.author {
    font-family: 'Georgia', serif;
    font-style: italic;
    font-size: 16px;
    color: #f5f2ff;
    margin-bottom: 8px;
}

/* Link styling */
.link {
    font-size: 16px;
    color: #bfa3ff;
    text-decoration: none;
    font-weight: 600;
}

.link:hover {
    text-decoration: underline;
    color: #d8c4ff;
    cursor: pointer;
}

/* Image styling */
.article-image {
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.4);
    margin-bottom: 15px;
    transition: transform 0.3s ease;
}

.article-image:hover {
    transform: scale(1.02);
}

/* Horizontal line styling */
hr {
    margin: 30px 0;
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>


# 🧠 AI News Scraper

<|Press the button below to scrape the latest AI news from TechCrunch.|>

<|Scrape AI News|button|on_action=scrape_ai_news|>

### Article 1

<|{title1}|text|class_name=title|>


<|{author1}|text|class_name=author|>

<|Read More: {link1}|text|class_name=link|>

<|{image1}|image|height=200px|class_name=article-image|>
<hr/>

### Article 2

<|{title2}|text|class_name=title|>

<|{author2}|text|class_name=author|>

<|Read More: {link2}|text|class_name=link|>

<|{image2}|image|height=200px|class_name=article-image|>
<hr/>

### Article 3

<|{title3}|text|class_name=title|>

<|{author3}|text|class_name=author|>

<|Read More: {link3}|text|class_name=link|>

<|{image3}|image|height=200px|class_name=article-image|>
<hr/>

### Article 4

<|{title4}|text|class_name=title|>

<|{author4}|text|class_name=author|>

<|Read More: {link4}|text|class_name=link|>

<|{image4}|image|height=200px|class_name=article-image|>
<hr/>

### Article 5

<|{title5}|text|class_name=title|>

<|{author5}|text|class_name=author|>

<|Read More: {link5}|text|class_name=link|>

<|{image5}|image|height=200px|class_name=article-image|>
<hr/>

### Article 6

<|{title6}|text|class_name=title|>

<|{author6}|text|class_name=author|>

<|Read More: {link6}|text|class_name=link|>

<|{image6}|image|height=200px|class_name=article-image|>
<hr/>

### Article 7

<|{title7}|text|class_name=title|>

<|{author7}|text|class_name=author|>

<|Read More: {link7}|text|class_name=link|>

<|{image7}|image|height=200px|class_name=article-image|>
<hr/>

### Article 8

<|{title8}|text|class_name=title|>

<|{author8}|text|class_name=author|>

<|Read More: {link8}|text|class_name=link|>

<|{image8}|image|height=200px|class_name=article-image|>
<hr/>

### Article 9

<|{title9}|text|class_name=title|>

<|{author9}|text|class_name=author|>

<|Read More: {link9}|text|class_name=link|>

<|{image9}|image|height=200px|class_name=article-image|>
<hr/>

### Article 10

<|{title10}|text|class_name=title|>

<|{author10}|text|class_name=author|>

<|Read More: {link10}|text|class_name=link|>

<|{image10}|image|height=200px|class_name=article-image|>
<hr/>

"""

Gui(page).run(port=5020)
# scrape_ai_news("")