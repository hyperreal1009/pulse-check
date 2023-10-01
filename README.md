# 🌐 PulseCheck

#### "Keep your bookmarks' pulse in check! 📚💔"

## 🚀 Overview

PulseCheck is a Python script that helps you manage your bookmarks in the most awesome way possible. It checks your list for dead links, keeping only the lively ones, and archives the dead links for you. If you're the type who bookmarks anything and everything, PulseCheck is your new best friend! 😍

## 📜 About

PulseCheck is your ultimate bookmark management utility. Written in Python, this script checks your bookmarks for dead or unreachable links, separates the good from the bad, and even lets you archive the URLs that are no longer working. 🧙‍♂️

## 🌟 Features

- 📋 Read HTML bookmarks file.
- 🔗 Check the pulse of each bookmark.
- 🗑️ Archive dead bookmarks.
- 💚 Keeps your bookmark list lean and mean!
- 🕐 Customizable timeout for link checking.
- 🤖 Smart-mode to prevent being flagged as a bot.
- 📝 Verbose and non-verbose logging options.

## 🛠️ Installation

1. Clone the repo or download the source code.
   ```bash
   git clone https://github.com/your-username/PulseCheck.git
   ```
2. Navigate into the project folder and install the required packages.
   ```bash
   cd PulseCheck
   pip install -r requirements.txt
   ```

## 🛠️ Usage

Here are the ways you can make PulseCheck work for you!

### Basic Usage
```bash
python pulsecheck.py
```

### With Arguments 🌈

Here's what each argument does:

#### `--filename`
- **Description**: Specify the HTML bookmark file you want to check.
```bash
python pulsecheck.py --filename=yourfile.html
```

#### `--timeout`
- **Description**: Set the maximum time, in seconds, for each link to respond.
```bash
python pulsecheck.py --timeout=10
```

#### `--smart-mode`
- **Description**: Enable this to randomize the timeout between 5 to 10 seconds, reducing the chance of getting flagged as a spam bot.
```bash
python pulsecheck.py --smart-mode
```

#### `--verbose`
- **Description**: Show all logs if enabled. If not, you'll just see a counter (e.g., "1/1000 bookmarks checked").
```bash
python pulsecheck.py --verbose
```

#### `--no-archive`
- **Description**: If enabled, the script will not create a `dead_links.txt` file to store dead links.
```bash
python pulsecheck.py --no-archive
```

## 📝 Requirements

- Python 3.x
- BeautifulSoup
- Requests library

## 🌟 Features

- 📋 Read HTML bookmarks file.
- 🔗 Check the pulse of each bookmark.
- 🗑️ Archive dead bookmarks.
- 💚 Keeps your bookmark list lean and mean!

## 📝 Changelog
[v1.2.0] - 2023-10-01
Added
--purge argument to remove invalid links before checking, also generates a .bak backup file.
Enhanced logging during the purging process.
Dead links and other status codes are now archived in HTML format for easy upload to a browser.
Detailed argument description in the README file.
[v1.1.0] - 2023-09-25
Added
--filename argument to specify a custom bookmarks file path.
--timeout argument for specifying the request timeout in seconds.
--smart-mode argument to randomize timeouts to avoid spam flags.
--verbose argument for verbose logging.
--no-archive argument to disable dead link archiving.
Changed
Updated check_links to also capture other status codes besides 200 and 404.
[v1.0.0] - 2023-09-20
Added
Initial version of PulseCheck.
Supports reading an HTML file of bookmarks.
Checks each link for a 200 HTTP status code.
Archives dead links in a dead_links.txt file.
Creates a new HTML file with live links only.


## 👥 Contribution

Feel free to fork, improve, create issues or pull requests (they're always welcome).

## 📄 License

This project is open-source and available under the MIT License.
