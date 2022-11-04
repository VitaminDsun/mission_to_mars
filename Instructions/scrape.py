from dataclasses import dataclass
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)

    
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        # 'mars_news': mars_news(browser),
        'featured_image': featured_image(browser),
        'mars_facts': mars_facts(),
        'hemispheres': hemispheres(browser)
    }
    browser.quit()


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find_all('img', class_='fancybox-image')[0]['src']
    featured_image_url = f'{url}{image}'
    browser.quit()

    def mars_news(browser):
    
    # Scrape Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = bs(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text') 
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    url = "https://spaceimages-mars.com"
    browser.visit(url)
    button = browser.find_by_tag("button")[1]
    button.click()
    img_soup = bs(browser.html, "html.parser")
    try:
        img_url = img_soup.find('img', class_="fancybox-image").get("src")
    except AttributeError:
        return None
    src_url = f'https://spaceimages-mars.com/{img_url}'
    return src_url
def mars_facts():
    try:
        mars_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    except BaseException:
        return None
    mars_df.columns = ["description", "mars", "earth"]
    mars_df.set_index("description", inplace=True)
    mars_df.to_html()
    return mars_df.to_html(classes='table table-striped')
def hemispheres(browser):
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    hemispheres = []
    for item in range(4):
        #Click into image, Get title, Get image url, dding to dictionary
        browser.find_by_css("a.product-item img")[item].click()
        title = browser.find_by_css('h2.title').text
        element= browser.links.find_by_text("Sample").first
        img_url = element["href"]
        hemisphere_dict = {}
        hemisphere_dict["title"] = title
        hemisphere_dict["img_url"] = img_url
        hemispheres.append(hemisphere_dict)
        browser.back()
    return hemispheres
if __name__ == '__main__':
    print(scrape_all())


#'worked with TA's and Other students to develop code and also looked some stuff up onon stackoverflow to help me find the answers need to get the right idea going'