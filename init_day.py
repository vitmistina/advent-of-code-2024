import os
import sys
import requests
from dotenv import load_dotenv

def read_template(template_name):
    with open(template_name, 'r') as f:
        return f.read()

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

    # Create __init__.py file
    with open(init_file, 'w') as f:
        pass

    # Create main file
    with open(main_file, 'w') as f:
        f.write(main_template.format(year=year, day=day))

    # Create test file
    with open(test_file, 'w') as f:
        f.write(test_template.format(year=year, day=day))

    # Create empty test input file
    with open(test_input_file, 'w') as f:
        pass

    # Download input file
    url = f"https://adventofcode.com/{year}/day/{int(day)}/input"
    cookies = {'session': os.getenv('SESSION_COOKIE')}
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        with open(input_file, 'w') as f:
            f.write(response.text)
    else:
        print(f"Failed to download input file: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python init_day.py YYYY-dd")
    else:
        initialize_day(sys.argv[1])