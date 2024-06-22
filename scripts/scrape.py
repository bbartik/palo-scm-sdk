from bs4 import BeautifulSoup

# Load the HTML content from the file
with open('api_endpoints.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Parse the HTML content
soup = BeautifulSoup(content, 'lxml')

# Find all the anchor tags within list items and extract their href attributes
endpoints = []
for li in soup.find_all('li', class_='theme-doc-sidebar-item-category'):
    a_tag = li.find('a', class_='menu__link')
    if a_tag and 'href' in a_tag.attrs:
        endpoints.append(a_tag['href'])

# Print or save the endpoints
for endpoint in endpoints:
    print(endpoint)

with open('api_endpoints.txt', 'w', encoding='utf-8') as output_file:
    for endpoint in endpoints:
        output_file.write(f"{endpoint}\n")

