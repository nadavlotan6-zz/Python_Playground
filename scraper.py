from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=graphics+cards&N=-1&isNodeId=1'

# opening a connection and grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, 'html.parser')

# grabbing each products
containers = page_soup.findAll("div", {"class":"item-container"})

filename = "products.csv"
f = open(filename, "w")

headers = "product_name\n"

f.write(headers)

for container in containers :
	title_container = container.findAll("a", {"class":"item-title"})
	product_name = title_container[0].text.strip()


	print("Product Name: " + product_name)
	f.write(product_name.replace(",", "|") + "\n")

f.close()







