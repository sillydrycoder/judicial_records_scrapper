# Automation Bot for Judicial Records Scraping

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Overview
The **Automation Bot** is a Python-based tool designed to scrape judicial records from the Poder Judicial website. The bot automates the process of searching for specific records based on user-defined criteria, retrieving search results, and handling various tasks, such as validating input data, managing cookies, and logging operations. This bot is intended for use by legal professionals, researchers, and developers who need to automate data retrieval processes from judicial databases.

## Features
- **Automated Data Retrieval**: Searches judicial records based on user-defined search strings and jurisdictions.
- **CSV Validation**: Ensures the integrity of input data before processing.
- **Cookie Management**: Automatically obtains and manages session cookies for authenticated requests.
- **Error Handling**: Comprehensive logging and error handling mechanisms ensure robust operation.
- **Headless Browser Support**: Uses Chrome in headless mode for efficient and unobtrusive operation.
- **Cross-Platform Compatibility**: Supports Windows, macOS, and Linux.

## Prerequisites
Before using this bot, ensure you have the following installed on your system:
- Python 3.7+
- Google Chrome (latest version)
- ChromeDriver (if `use_chromedriver` is set to `True` in `config.json`)
- pip (Python package manager)

The bot also requires the following Python packages:
- `selenium`
- `requests`
- `beautifulsoup4`
- `colorama`

You can install these packages using the following command:
```bash
pip install -r requirements.txt
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tensor35/judicial_records_scrapper.git
   cd judicial_records_scrapper
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your `entries.csv` file in the root directory of the project. This file should contain the search queries and corresponding jurisdictions.

## Configuration
The bot requires a configuration file named `config.json`, which should be placed in the root directory. The configuration file includes settings such as available jurisdictions and the option to use a custom ChromeDriver. Below is an example configuration:

```json
{
    "use_chromedriver": true,
    "available_jurisdiction": ["Civil", "Criminal", "Administrative"],
    "heading": "Judicial Records Automation Bot"
}
```

- `use_chromedriver`: Set to `true` to use a custom ChromeDriver; otherwise, set to `false`.
- `available_jurisdiction`: List of valid jurisdictions that can be used in the `entries.csv` file.
- `heading`: Custom heading displayed in the terminal during bot execution.

## Usage
To start the bot, run the following command in the terminal:

```bash
python automamtion_bot_v1.py
```

The bot will guide you through the process, including validating the input CSV file, obtaining session cookies, and starting the scraping process. Ensure your terminal window is maximized for the best user experience.

### CSV File Structure
The `entries.csv` file should contain the following columns:
- **Search String**: The string to search for in the judicial records.
- **Jurisdiction 1**: The first jurisdiction to search within.
- **Jurisdiction 2**: The second jurisdiction to search within.
- **Jurisdiction 3**: The third jurisdiction to search within.
- **Total Results (Optional)**: This column will be populated by the bot during execution.

### Example `entries.csv`
```csv
Search Term 1,Civil,Criminal,Administrative,
Search Term 2,Criminal,Civil,Administrative,
```

## Logging
The bot uses Python's built-in logging module to capture detailed logs of its operations. Logs are written to `script.log` in the root directory. The log file includes timestamps, log levels, and detailed messages about each step of the process.

### Log Levels
- **INFO**: General information about the bot's operation.
- **ERROR**: Captures any errors encountered during execution.
- **DEBUG**: (If enabled) Detailed debugging information for troubleshooting.

## Error Handling
The bot includes comprehensive error handling mechanisms to ensure reliable operation. If any errors occur, the bot will log them in `script.log` and provide guidance in the terminal. In case of critical issues, the bot will gracefully exit, allowing the user to review logs and correct any problems.

### Common Errors
- **CSV Validation Errors**: If the input CSV file is invalid, the bot will log specific issues, such as missing files, incorrect column counts, or invalid jurisdictions.
- **Cookie Retrieval Errors**: If the bot fails to obtain a session cookie, it will attempt to refresh the page or restart the browser session.
- **ChromeDriver Errors**: If the ChromeDriver is missing or outdated, the bot will provide instructions for downloading the correct version.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue on GitHub if you have any suggestions, bug reports, or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

**Disclaimer**: This bot is provided for educational and research purposes only. The authors are not responsible for any misuse or legal implications arising from the use of this software.
