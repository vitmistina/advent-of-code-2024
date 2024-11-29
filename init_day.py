import os
import sys
import requests
from dotenv import load_dotenv

def read_template(template_name):
    try:
        with open(template_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        sys.exit(f"Template file {template_name} not found.")

def create_file(file_path, content=""):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError as e:
        sys.exit(f"Failed to create file {file_path}: {e}")

def download_input_file(url, cookies, input_file):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        with open(input_file, 'w') as file:
            file.write(response.text)
    except requests.RequestException as e:
        sys.exit(f"Failed to download input file: {e}")

def initialize_day(date):
    load_dotenv()
    year, day = date.split('-')
    day_folder = f"{year}_{day}"
    os.makedirs(day_folder, exist_ok=True)

    init_file = os.path.join(day_folder, '__init__.py')
    main_file = os.path.join(day_folder, f"aoc_{year}_{day}.py")
    test_file = os.path.join(day_folder, f"test_{year}_{day}.py")
    input_file = os.path.join(day_folder, f"{year}_{day}_input.txt")
    test_input_file = os.path.join(day_folder, f"{year}_{day}_test.txt")

    main_template = read_template('main_template.txt')
    test_template = read_template('test_template.txt')

    create_file(init_file)
    create_file(main_file, main_template.format(year=year, day=day))
    create_file(test_file, test_template.format(year=year, day=day))
    create_file(test_input_file)

    url = f"https://adventofcode.com/{year}/day/{int(day)}/input"
    cookies = {'session': os.getenv('SESSION_COOKIE')}
    download_input_file(url, cookies, input_file)    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python init_day.py YYYY-dd")
    initialize_day(sys.argv[1])