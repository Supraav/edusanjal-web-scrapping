
import requests
from bs4 import BeautifulSoup as bs
import requests
import json
import time

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
website = 'https://edusanjal.com/college'

result = requests.get(website,headers=HEADER)
content = result.text
edusanjal = bs(content,"lxml")
# print(soup.prettify())
# print(soup.head.title)

urls=[]
main_div = edusanjal.find('div', class_='grid gap-8 md:grid-cols-2 lg:grid-cols-3 lg:max-w-full')
div_list = main_div.find_all('div', class_='overflow-hidden bg-white rounded shadow-xl')

for div in div_list:
    link = div.find('a')['href']
    link = link[8:]
    total_url= website+link
    urls.append(total_url)
# print(urls)


result=[]
for url in urls:
    # print(url)
    time.sleep(6)
    response = requests.get(url,headers=HEADER)
    html_content = response.text
    soup = bs(html_content,"lxml")

    #title
    title_finder=soup.find('div',class_ = 'org-title')
    title=soup.find('div',class_ = 'org-title').h1.text.strip()
    title=title[:-2]
    # print(title)

    #address
    address=title_finder.find('div',class_='text-base')
    address_location = address.span.get_text() 
    location=address_location.split(' ')
    # print(location)


    #street line address
    street_line_address=''.join(location)
    # print(street_line_address)
    if len(location) > 2:    
        city=location[0:-1]
        district=location[-1]
    else:
        city=location[0]
        district=location[1]



    #latitude and longitude
    direction=soup.find('div',id='map')
    map_link = direction.find('a')['href']
    coordinates = map_link.split('?q=')[1].split(',')
    latitude = coordinates[0]
    longitude = coordinates[1]
    # print(latitude,longitude)


    #right column
    right_column=soup.find('div',class_='org-right')


    #email
    email_tag=right_column.find('li',title='Email')
    email_element = email_tag.span.get_text()
    # print(email_element)


    #phone number
    phone_tag=right_column.find('li',title='Phone')
    phone_element = phone_tag.span.get_text().replace(',','|').replace('&','|').replace(' ','').split('|')
    # print(phone_element)


    #logos
    logos=soup.select_one('img.max-h-48.mb-1.md\:-mb-8.rounded-r-3xl.md\:shadow-xl.p-4.md\:bg-white')['src']
    # print(logos)


    #cover image
    coverimage=soup.select_one('img.object-scale-down.w-full.mh-300')['src']
    # print(coverimage)


    #about
    about_main=soup.select_one('.content.mt-4.col-span-3.pr-8')
    about_text=about_main.select_one('.prose.max-w-none.text-gray-600 ').text
    # print(about_text)


    #websiteURL
    url=right_column.select_one('a.inline-flex.justify-center.h-12.w-12.text-lg.hover\:text-gray-800')['href']
    # print(url)


    #established date
    est_date=right_column.find('li',title='Established')
    try:
        est_list= est_date.span.get_text().split(' ')
        est=est_list[1]+' '+est_list[2]
    except:
        est=''
    # print(est)



    #ownership type
    ownership_type_find=right_column.find('li',title='Ownership')
    ownership_type= ownership_type_find.span.get_text()
    # print(ownership_type)



    #gallery
    gallery_find = soup.find('div', id='gallery')
    gallery_photos = gallery_find.find_all('img')
    gallery = [photo['src'] for photo in gallery_photos]
    # print(gallery)


    #scholarship
    scholarship_find=soup.find('div',id='scholarship_information')
    try:

        scholarship_div=scholarship_find.select_one('.prose.max-w-none.text-gray-600').ul
        scholarship_items = [item.text.strip() for item in scholarship_div if item.text.strip()]
    except:
        scholarship_items=[]
    # print(scholarship_items)


    #affiliated to 
    affiliated=[]
    universities = soup.select('li[title="Accreditation"]')
    for university in universities:
        try:
            name = university.select_one('a > span:last-child').text.strip()
            affiliated.append(name)
        except:
            affiliated=[]
        
    # print(affiliated)



    #data
    data = {
        'title': title,
        'address':
        {
            'country_name': 'Nepal',
            'city':city,
            'district':district,
            'street_line_address':street_line_address,
            'latitude':latitude,
            'longitude':longitude,
        },
        'email':email_element,
        'contact':phone_element,
        'logo':logos,
        'coverimage':coverimage,
        'about':about_text,
        'websiteURL':url,
        'established':est,
        'organization_type':'college',
        'ownership_type':ownership_type,
        'gallery':gallery,
        'scholarship':
        {
            'title':scholarship_items,
        },
        
    }
    result.append(data)
    
output_file = 'result.json'
# result_json = json.dumps(data, indent=4)
# Save the JSON data to a file
with open(output_file, 'w') as file:
    # file.write(result_json, file)
    json.dump(result, file)

print('JSON data saved to', output_file)
print(result)