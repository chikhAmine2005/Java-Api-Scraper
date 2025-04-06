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

    packages = []

    for a in soup.select('a[href$="package-summary.html"]'):  # Select links ending with "package-summary.html"
        name = a.text.strip()
        if name.count(".") < 2:  # Filter out packages with more than one dot
            packages.append(name)

    return packages

# Get module links
module_links = get_module_links()

# Get package names for each module
all_packages = []
for module_name, module_url in module_links.items():
    package_names = get_packages(module_name, module_url)
    all_packages.extend(package_names)

# Write the package names to a JSON file
with open('package_names.json', 'w') as json_file:
    json.dump(all_packages, json_file, indent=4)

print("Package names have been written to package_names.json")

