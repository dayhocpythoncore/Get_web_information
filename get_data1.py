from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

query = input('Enter search query:\n')
search = query.replace(" ", "%20")
my_url = 'https://www.flipkart.com/search?q=' + search + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
print(my_url)
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

number_element = page_soup.findAll("span", {"class": "_10Ermr"})
for val in number_element:
    list_data = str(val).split(' ')
    page_number = (int(list_data[6].replace(',', '')) // 24) + 1
    break
print(page_number)

for i in range(1,page_number+1):
    my_url = 'https://www.flipkart.com/search?q=' + search + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='+str(i)
    print(my_url)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")



    containers = page_soup.findAll("div", {"class": "_2kHMtA"})

    filename = "products.csv"
    f = open(filename, "a")  # mở file chế độ ghi tiếp

    headers = "Product Name,Price,Rating" + "\n"
    f.write(query + "\n")  # Display search Query on csv file
    f.write(headers + "\n")

    for container in containers:
        # for getting name
        product_name = container.div.img["alt"]
        product_name = product_name.replace(",", " | ")  # replacing comas cause in csv coma seperates different values
        print(product_name)

        # for getting price
        price_container = container.findAll("div", {"class": "_30jeq3 _1_WHN1"})
        try:
            price = price_container[0].text.replace("₹", "Rs ")
            price = price.replace(",", "")  # replacing comas cause in csv coma seperates different values
            print(price)
        except (IndexError, ValueError):
            pass

        # for getting rating
        rating_container = container.findAll("div", {"class": "_3LWZlK"})
        try:  # to solve index error in certain cases
            rating = rating_container[0].text + "*"
            rating = rating.replace(",", "")  # replacing comas cause in csv coma seperates different values
            print(rating, "\n")
        except (IndexError, ValueError):
            pass

        f.write(product_name + "," + price + "," + rating + "\n")  # writing to file
        print('success one')
