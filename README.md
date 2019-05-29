# Topos
Topos - Web Scraping Assignment

Please run the file "wiki_webscraping.py" which serves as a scraper in python to collect data from "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population" link and associated wiki webpages for each city from the first link.

Requisites : This project requires python 3 environment with "requests" "BeautifulSoup4" and "pandas" libraries pre-installed. If not, they maybe be installed via "pip install requests BeautifulSoup4 pandas".

Note : Please change the local path in the last line of "wiki_webscraping.py" where you would like to save output CSV file and use "Google Sheets" to view the file.

  This output file is tested to upload to BigQuery table and the query result is posted as a snapshot in "Results" folder. The "Results" folder also contains the output file by running the python code and sample visualization of BigQuery Table data on "Google Data Studio".

Approach : From the given webpage, the main table containing data of all the popular cities has been captured. All the table data "td" tags of this table are fetched and processed one by one. The data must be cleaned to obtain the same text as seen on webpage and hemce I used regular expression substitutions. Since we know the column names and structure of table, each data field is appended to respective value list for each key of the dictionary. This dictionary has additional keys/columns added apart from the given weblink. This is to demonstrate supplementing additional information from other webpages. This can be observed in the project as "Official_Website" key of the dictionary. For each of the city in the table, we scrape the wiki link of that city by fetching the "href" attribute of "a" tag. This link is inturn scraped to find another table, that contains a summary of the city. I have captured the "Website" field from this table and added it to our dictionary as a value field for "Official_Website" column. After this process has been done for 314 popular (populous) cities, the dictionary is loaded to a "pandas" dataframe. As per our interest, we can print the dataframe and also save the contents locally to a CSV file.

I have chosen "Official_Website" as additional field since I believe, each city has most accurate, historic, latest and consolidated information on their official webpages. Further scraping these websites would be really helpful in knowing more about them. The downside however, I observed is that these government websites do not provide certain categories of information that are best provided by social media platforms like how residents, visitors engage themselves and interact with the city in real-time. I believe an approach towards integrating information from government and social media resources could provide much more valuable insights in learning about a city environment and it's people.
