import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://docs.oracle.com/en/java/javase/17/docs/api/"


def get_module_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    modules = {}

    for a in soup.select('a[href$="module-summary.html"]'):  # Select links ending with "module-summary.html"
        href = a['href']
        name = a.text.strip()
        if name.startswith("java.") or name.startswith("javax."):  # Filter out unwanted modules
            full_url = BASE_URL + href
            modules[name] = full_url

    return modules


def get_packages(module_name, module_url):
    response = requests.get(module_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    packages = {}

    for a in soup.select('a[href$="package-summary.html"]'):  # Select links ending with "package-summary.html"
        href = a['href']
        name = a.text.strip()
        if name.count(".") < 2:  # Filter out packages with more than one dot
            full_url = BASE_URL + module_name + '/' + href
            packages[name] = full_url
    return packages


module_links = get_module_links()
# test module links
for name, link in list(module_links.items())[:]:
    print(f"{name}: {link}")

# test package links
for module_name, module_url in list(module_links.items())[:]:
    print(f"\nPackages in {module_name}:")
    package_links = get_packages(module_name, module_url)
    for name, link in list(package_links.items())[:]:
        print(f"{name}: {link}")


# Write the package names links to a JSON file
with open('package_links.json', 'w') as json_file:
    json.dump(package_links, json_file, indent=4)
print("Package links have been written to package_links.json")

