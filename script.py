import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        full_url = BASE_URL + module_name + '/' + href
        packages[name] = full_url

    return packages

def get_types(package_url):
    response = requests.get(package_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    types = {}

    for a in soup.select('a[href$=".html"][title]'):  # Select links ending with ".html" and having 'title'
        href = a['href']
        name = a.text.strip()
        title = a.get('title', '')
        type_info = title.split(' ')[0] if title else "unknown"  # Extract the type (class, interface, etc.)
        full_url = package_url.rsplit('/', 1)[0] + '/' + href
        types[name] = {'type': type_info, 'url': full_url}

    return types

def process_module(module_name, module_url):
    package_links = get_packages(module_name, module_url)
    module_data = {}
    for package_name, package_url in package_links.items():
        types = get_types(package_url)
        if package_name not in module_data:
            module_data[package_name] = {"class": [], "interface": [], "enum": [], "annotation": []}
        for type_name, type_info in types.items():
            type_category = type_info['type']
            if type_category == "class":
                module_data[package_name]["class"].append(type_name)
            elif type_category == "interface":
                module_data[package_name]["interface"].append(type_name)
            elif type_category == "enum":
                module_data[package_name]["enum"].append(type_name)
            elif type_category == "annotation":
                module_data[package_name]["annotation"].append(type_name)
    return module_data

# Get module links
module_links = get_module_links()

all_data = {}

# Use ThreadPoolExecutor to process modules concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_module = {executor.submit(process_module, module_name, module_url): module_name for module_name, module_url in module_links.items()}
    for future in as_completed(future_to_module):
        module_name = future_to_module[future]
        try:
            module_data = future.result()
            all_data.update(module_data)
        except Exception as exc:
            print(f'{module_name} generated an exception: {exc}')

# Write the package names to a JSON file
with open('all_data.json', 'w') as json_file:
    json.dump(all_data, json_file, indent=4)

print("All data has been written to all_data.json")