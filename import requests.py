import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
import os


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/16.16299",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
]

def getRandomUserAgent():
    return random.choice(user_agents)

reviewlist = []

def getRandomProxy():
    # Using Proxy 
    proxy = {
        "http": f"http://yzUfquvEcmDmwEMi:wifi;;;;@proxy.soax.com:{9000 + random.randint(0, 5000)}",
        "https": f"http://yzUfquvEcmDmwEMi:wifi;;;;@proxy.soax.com:{9000 + random.randint(0, 5000)}"
    }
    return proxy
 
def extractReviews(reviewUrl, pageNumber):
    
    try:
        headers = {
            'User-Agent': getRandomUserAgent()  # Get a random User-Agent
        }
        resp = requests.get(reviewUrl, proxies=getRandomProxy())
    except Exception as e:
        print(f"Error while making the request: {e}")
    print ("Response first time server check")
    print (resp)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.findAll('div', {'data-hook':"review"})
    print(soup.prettify())
    print(reviews)
    for item in reviews:
        print (item)
        # with open('outputs/file.html', 'w', encoding='utf-8') as f:
        #     f.write(str(item))
        
        review = {
            'productTitle': soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip(),
            'Review Title': item.find('a', {'data-hook':"review-title"}).text.strip(),
            'Rating': item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
            'Review Body': item.find('span', {'data-hook': 'review-body'}).text.strip() ,
        }
        print(review['Review Title'])
        reviewlist.append(review)  

def totalPages(productUrl):
    try:
        headers = {
            'User-Agent': getRandomUserAgent()
        }
        resp = requests.get(productUrl, proxies=getRandomProxy())
    except Exception as e:
        print(f"Error while making the request: {e}")
    print (resp)
    soup = BeautifulSoup(resp.text, 'html.parser')
    reviews = soup.find('div', {'data-hook': "cr-filter-info-review-rating-count"}) 
    
    if reviews is not None:
        return int(reviews.text.strip().split(', ')[1].split(" ")[0])
    else:
        # Handle the case when no reviews are found on the page
        # print (reviews)
        return 0
def main():
    productUrl = "https://www.amazon.in/Amazon-Brand-Vedaka-Mango-Pickle/dp/B093L7VPQL"
    reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(1)
    totalPg = totalPages(reviewUrl)
    print ("check here")
    print(totalPg)
    
    # range for i changed at 10:13 am
    for i in range(1, totalPg//10 + 1 ):
    # in range(1):
        print(f"Running for page {i}")
        try: 
            reviewUrl = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(i)
            print ("reviewUrl"+reviewUrl)
            extractReviews(reviewUrl, i)
            print ("entering for loop")
        except Exception as e:
            print(e)

        wait_time = random.uniform(10, 25)
        print(f"Waiting for {wait_time:.2f} seconds before the next request...")
        time.sleep(wait_time)
        

    desktop_path = os.path.expanduser('~/Desktop')  # Get the path to the desktop
    excel_file_path = os.path.join(desktop_path, 'Amazon_Reviews.xlsx')  # Specify the Excel file path on the desktop
    
   
    df = pd.DataFrame(reviewlist)
    df.to_excel(excel_file_path, sheet_name='Amazon_Reviews', index=False)

main()



# amazon is unable to get cookies through these hits 
# 503 through the proxy code
# in case of 503 retry the code
# multiple links to be serviced in single query