import requests
import xml.etree.ElementTree as ET
import pandas as pd

# Fetch the RSS feed
url = "https://www.dailyforex.com/rss/technicalanalysis.xml"
url1 = "https://www.dailyforex.com/rss/forexnews.xml"

response = requests.get(url)
root = ET.fromstring(response.content)
items = root.findall(".//item")
data = []
for item in items:
    entry = {
        "title": item.findtext("title"),
        "author": item.findtext("author"),
        "link": item.findtext("link"),
        "pubDate": item.findtext("pubDate"),
        "description": item.findtext("description")    }
    data.append(entry)
df = pd.DataFrame(data)
df = df[["pubDate","title","description"]]
df["pubDate"] = pd.to_datetime(df["pubDate"])  
df ["pubDate"] = df["pubDate"].dt.strftime("%Y-%m-%d %H:%M")
df.to_csv("data/forexnews.csv",index=False)
print(df.head(20))

#--------------------
# Step 1: Fetch the RSS feed
url = "https://www.myfxbook.com/rss/latest-forex-news"
url = "https://www.fxstreet.com/rss/analysis"
url = "https://www.fxstreet.com/rss"
response = requests.get(url)
response.raise_for_status()
root = ET.fromstring(response.content)
items = root.findall(".//item")
data = []
for item in items:
    data.append({
        "title": item.findtext("title"),
        "link": item.findtext("link"),
        "pubDate": item.findtext("pubDate"),
        "description": item.findtext("description")    })
df = pd.DataFrame(data)
df = df[["pubDate","title","description"]]
df["pubDate"] = pd.to_datetime(df["pubDate"])  
df ["pubDate"] = df["pubDate"].dt.strftime("%Y-%m-%d %H:%M")
print(df.head(60))

