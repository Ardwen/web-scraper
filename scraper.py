import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import re


def rating_page(url,f):
 uClient=uReq(url)
 dpage = uClient.read()
 uClient.close()
 dpage_soup = soup(dpage,"html.parser")
 #all rates
 all_rate = dpage_soup.findAll("div", {"class": "inline-block ratings-imdb-rating"})[0].span.text
 #detailed rating number
 table = dpage_soup.findAll("div", {"class": "leftAligned"})
 rating_number = [k.text.replace(",","") for k in table][1:11]
 #detailed demographic number
 div_list = dpage_soup.findAll('td',attrs={"align":"center"})
 value = [k.find('div', attrs={'class':'bigcell'}).text.strip() for k in div_list]
 num = [k.find('div', attrs={'class':'smallcell'}).text.strip().replace(",","") for k in div_list]
 #scores=pd.DataFrame({'value':value,'num':num})
 f.write("," + ",".join(rating_number) + "," + ",".join(value)+ "," + ",".join(num) + "\n")

def mainpage(url):
 uClient = uReq(url)
 page = uClient.read()
 uClient.close()

 #html parsing
 page_soup = soup(page,"html.parser")

 #rating information

 #the detailed rating page
 detail = page_soup.findAll("div", {"class": "imdbRating"})
 rating_url = 'https://www.imdb.com' + detail[0].a["href"]

 #season, director, characters
 seas = page_soup.find("div", {"class": "bp_heading"}).text[7]
 episode = page_soup.find("div", {"class": "bp_heading"}).text[-1]
 episode_name = page_soup.findAll("div", {"class": "title_wrapper"})[0].h1.text
 print(episode_name)
 story_line = page_soup.findAll("div", {"class": "inline canwrap"})[0].p.span
 director = page_soup.findAll("div", {"class": "credit_summary_item"})[0].a.text
 character = page_soup.findAll("td", {"class": "character"})
 character_name = [i.text.strip().replace("\n","") for i in character]
 f.write(episode_name + "," + seas + "," + episode + "," + director + "," + "|".join(character_name))
 rating_page(rating_url, f)


filename = "product.csv"
f = open(filename,"w")
#write the headers
headers = "name,season,episode, direcotrdirector,characters,rate_10,rate_9,rate_8,rate_7,rate_6,rate_5," \
          "rate_4,rate_3,rate_2,rate_1,all_rate,<18,18-29,30-44,45+,all_rate(m),<18(m),18-29(m),30-44(m),45+(m),all_rate(f),<18(f),18-29(f),30-44(f),45+(f)," \
          "top1000,us_user,non_us" \
          "all_rate(#),<18(#),18-29(#),30-44(#),45+(#),all_rate(m#),<18(m#),18-29(m#),30-44(m#),45+(m#),all_rate(f#),<18(f#),18-29(f#),30-44(f#),45+(f#)," \
          "top1000(#),us_user(#),non_us(#)\n"
f.write(headers)
seasons = ["https://www.imdb.com/title/tt0944947/episodes?season="+ str(k) for k in range(1,9)]
for season in seasons:
 uClient=uReq(season)
 spage = uClient.read()
 uClient.close()
 spage_soup = soup(spage,"html.parser")
 scontainer = spage_soup.findAll("div", {"class": "list detail eplist"})
 pattern = re.compile("title/tt[1-9]\d{6}/")
 a = pattern.findall(str(scontainer))
 urls = ["https://www.imdb.com/" + k for k in list(set(a))]
 for mainp in urls:
  print(mainp)
  mainpage(mainp)
f.close()