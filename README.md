# Automation Bot for Judicial Records Scraping (v2)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [License](#license)

## Overview
The **Automation Bot for Judicial Records Scraping** is a Python-based application that automates the process of searching and retrieving judicial records from the Poder Judicial website. Version 2 of the bot introduces several improvements and simplifications, including updates to configuration management and error handling.

## Features
- **Automated Record Search**: Searches for judicial records based on user-defined search terms and selected jurisdictions.
- **Headless Browser Operation**: Uses Chrome in headless mode for efficient operation.
- **Logging**: Detailed logging of bot activities and errors.
- **Flexible GUI**: Built using Tkinter with Pygubu Designer for a user-friendly interface.
- **CSV Output**: Saves search results to a CSV file.

## Prerequisites
Ensure you have the following installed:
- Python 3.7 or later
- Google Chrome (latest version)

Install the required Python packages using:
```bash
pip install selenium requests beautifulsoup4 pygubu
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tensor35/judicial_records_scrapper.git
   cd judicial_records_scrapper
   ```
2. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To start the bot, run the following command:
```bash
python main.py
```

### User Interface
The application features a Tkinter-based GUI that allows users to:
- Enter a search term.
- Select relevant jurisdictions via checkboxes.
- Start the search process.
- View progress and results in real-time.
- Open the GitHub repository for more information.

### CSV Output
Search results are saved in a `results.csv` file located in the root directory of the project. The file includes columns for:
- **Search String**
- **Jurisdictions**
- **Results**

## Logging
The bot uses Python's logging module to create detailed logs of its operations. Logs are stored in `script.log` in the root directory.

## Error Handling
The bot has built-in error handling to manage various issues:
- **Initialization Errors**: Issues with starting the bot or obtaining cookies are logged, and users are notified through the GUI.
- **Search Errors**: Problems during search operations are logged and displayed.

## Changelog
### v2.0
- **Removed Configuration File**: The bot no longer uses a `config.json` file.
- **CSV Output**: Results are now appended to a `results.csv` file.
- **Chromedriver Removal**: The bot no longer relies on a separate Chromedriver executable; it uses the default Chrome installation.
- **Simplified Dependencies**: Removed unnecessary dependencies and streamlined the setup process.

## Contributing
Contributions are welcome! Please submit issues or pull requests via GitHub for any bug fixes, improvements, or feature requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

**Disclaimer**: This bot is intended for educational and research purposes only. The authors are not responsible for any misuse or legal implications resulting from the use of this software.