# Java-Api-Scraper

This script scrapes the Oracle Java SE 17 API documentation to retrieve information about modules, packages, and types (classes, interfaces, enums, annotations). The data is organized and written to a JSON file.

## How It Works

1. **Retrieve Module Links**:
   - The `get_module_links` function fetches the main API page and extracts links to module summaries.
   - It filters out unwanted modules, keeping only those that start with "java." or "javax.".

2. **Retrieve Package Links**:
   - The `get_packages` function fetches each module summary page and extracts links to package summaries.
   - It constructs the full URL for each package summary.

3. **Retrieve Types**:
   - The `get_types` function fetches each package summary page and extracts types (class, interface, enum, annotation) based on the `title` attribute of the links.
   - It constructs the full URL for each type.

4. **Process Modules Concurrently**:
   - The `process_module` function processes each module by retrieving its packages and types.
   - It organizes the types into categories (class, interface, enum, annotation) for each package.
   - The script uses `ThreadPoolExecutor` to process modules concurrently, significantly reducing the overall runtime.

5. **Organize and Write Data**:
   - The script iterates through the modules and packages, categorizes the types, and stores them in a dictionary.
   - It writes the organized data to a JSON file named `all_data.json`.

## Usage

1. **Install Dependencies**:
   - Ensure you have `requests` and `beautifulsoup4` installed. You can install them using pip:
     ```sh
     pip install requests beautifulsoup4
     ```

2. **Run the Script**:
   - Execute the script to start the scraping process:
     ```sh
     python script.py
     ```

3. **Output**:
   - The script will create a JSON file named `all_data.json` containing the scraped data.

## Example Output

The JSON file will have a structure similar to this:

```json
{
    "javax.swing": {
        "class": ["JButton", "JLabel", ...],
        "interface": ["ActionListener", "ChangeListener", ...],
        "enum": [],
        "annotation": []
    },
    "javax.swing.table": {
        "class": ["AbstractTableModel", "DefaultTableModel", ...],
        "interface": ["TableModel", "TableCellRenderer", ...],
        "enum": [],
        "annotation": []
    }
}
```

## Notes

- The script is designed to handle a large number of requests efficiently by using multithreading.
- Ensure you have a stable internet connection as the script fetches data from the Oracle Java SE 17 API documentation website.

---
