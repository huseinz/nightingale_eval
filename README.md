# nightingale_eval

# Data Engineer Evaluation

## Overview
This evaluation is designed to assess your skills in integrating and manipulating data using Python and SQL. 
You will be working with a SQLite database (data.db) and tasked with importing data from both an API and a CSV file. 
Your performance will be evaluated based on the accuracy, efficiency, and cleanliness of your data integration process.

## Evaluation Ojectives
### Objective 1: API Data Integration
- Endpoint: `https://dummyjson.com/products`
- Tasks:
    - Retrieve data from the provided API endpoint.
    - Insert or update the retrieved data into the SQLite database.
    - Target Tables: `product`, `product_image`
- Solution:
    - Solution is contained in script `src/api_data.py` and writes records to `data/data.db`
    - The solution leverages `jsonschema` for input validation and `SQLAlchemy` for working with the database. 
    - Script prints the number of products written to the database.
    - There are some helper functions commented out in `__main__` for printing contents of tables and doing joins.
    - I implemented pagination of the product endpoint, so all 100 products are processed.

### Objective 2: CSV Data Integration
- Source File: `cities.csv`
- Tasks:
    - Create a new table within the SQLite database.
    - Import data from `cities.csv` into the newly created table.
- Solution:
    - Solution is contained in script `src/csv_integration.py`, reads records from `data/cities.csv` and writes records to `cities` table in `data/data.db`
    - The solution leverages `SQLAlchemy` for working with the database. 
    - Script prints the number of cities written to the database.
    - For simplicity, each time the script is run, it will truncate all records from the `cities` table before importing the CSV data.


### Objective 3: Data Extraction
- Output Format: CSV file
- Report Specifications:
    - Generate a report with the following columns:
        - `id`: Product ID
        - `title`: Product Title
        - `price`: Product Price
        - `image_count`: Number of images associated with the production
- Solution:
    - Solution is contained in script `src/extract_data.py`, reads records from `data/data.db` and writes records to `data/count_product_images.csv`
    - The solution leverages `SQLAlchemy` for working with the database. 
    - Script prints the number of products written to the CSV file.
    - For simplicity, each time the script is run, it will overwrite the contents of `data/count_product_images.csv`

## Deliverables

Upon completion of the tasks, the deliverable should consist of all the code used for the evaluation.
The code should be well-documented and structured for clarity and maintainability.
The following formats for submission are acceptable:

- **Zip File**: A compressed zip file containing all the necessary code files.
- **Git Repository**: A link to a Git repository (e.g., GitHub, GitLab, Bitbucket) containing the complete project.

Ensure that the repository is public or access is granted to the evaluator.
The submitted code will be reviewed for coding standards, logical structuring,
and adherence to the given tasks.

## Running the Deliverable

This solution was created using Python 3.12.0 but should be compatible with any Python version >= 3.7 that supports SQLAlchemy >= 2.0
It has been tested on Python 3.9.2 with SQLAlchemy==2.0.23

pip modules required:
```
requests~=2.31.0
SQLAlchemy~=2.0.23
jsonschema~=4.20.0
```

- Solution 1: `python src/api_data.py`
- Solution 2: `python src/csv_integration.py`
- Solution 3: `python src/extract_data.py`