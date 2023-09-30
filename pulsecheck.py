from bs4 import BeautifulSoup
import requests
import copy
import argparse
import random

# Step 2: Parse the HTML file


def read_bookmarks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    bookmarks = [(a['href'], a.get_text())
                 for a in soup.find_all('a', href=True)]
    return bookmarks, soup


# Step 3: Check Links
# ANSI color codes
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
PURPLE = '\033[95m'
RESET = '\033[0m'

# Archive other status links


def archive_other_status(other_status):
    with open('ignored.txt', 'w') as f:
        for link, title, status_code in other_status:
            f.write(f"{title}, {link}, {status_code}\n")


def archive_dead_links(dead_links):
    with open('dead_links.txt', 'w') as f:
        for link, title in dead_links:
            f.write(f"{title}, {link}\n")


# Step 5: Create new HTML with live links


def create_new_html(soup, dead_links):
    new_soup = copy.deepcopy(soup)
    for link in dead_links:
        bad_tag = new_soup.find('a', {'href': link})
        if bad_tag:
            bad_tag.extract()
    with open('cleaned_bookmarks.html', 'w', encoding='utf-8') as f:
        f.write(str(new_soup))


def main():
    parser = argparse.ArgumentParser(
        description='Check the health of your bookmarks.')

    parser.add_argument('--filename', default='bookmarks.html',
                        type=str, help='Path to the bookmarks HTML file.')
    parser.add_argument('--timeout', default=5, type=int,
                        help='Request timeout in seconds.')
    parser.add_argument('--smart-mode', action='store_true',
                        help='Randomize timeout to avoid spam flags.')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose logging.')
    parser.add_argument('--no-archive', action='store_true',
                        help='Disable archiving of dead links.')

    args = parser.parse_args()

    if args.smart_mode:
        timeout = random.randint(5, 10)
    else:
        timeout = args.timeout

    bookmarks, original_soup = read_bookmarks(args.filename)
    total_links = len(bookmarks)

    live_bookmarks, dead_bookmarks, other_status_bookmarks = check_links(
        bookmarks, timeout, args.verbose, total_links)

    if not args.no_archive:
        archive_dead_links(dead_bookmarks)
        archive_other_status(other_status_bookmarks)

    create_new_html(original_soup, [link for link, title in dead_bookmarks])

    print(f"{len(live_bookmarks)} live links kept.")
    print(f"{len(dead_bookmarks)} dead links archived.")
    print(f"{len(other_status_bookmarks)} links with other status codes.")


def check_links(bookmarks, timeout, verbose, total_links):
    dead_links = []
    live_links = []
    other_status = []

    for idx, (link, title) in enumerate(bookmarks, start=1):
        if verbose:
            print(
                f"{YELLOW}[CHECKING {idx}/{total_links}]:{RESET} {PURPLE}{title}{RESET} \n {link}")
        else:
            print(f"Checking {idx}/{total_links} bookmarks...")

        try:
            response = requests.get(link, timeout=timeout)
            if response.status_code == 200:
                if verbose:
                    print(f"{GREEN}[OK!]:{RESET} {PURPLE}{title}{RESET}")
                live_links.append((link, title))
            elif response.status_code == 404:
                if verbose:
                    print(f"{RED}[DEAD LINK]:{RESET} {PURPLE}{title}{RESET}")
                dead_links.append((link, title))
            else:
                if verbose:
                    print(
                        f"{RED}[OTHER STATUS {response.status_code}]:{RESET} {PURPLE}{title}{RESET}")
                other_status.append((link, title, response.status_code))
        except requests.RequestException as e:
            if verbose:
                print(
                    f"{RED}Error occurred while checking link: {PURPLE}{title}{RESET} \n ({link}). \nError: {e}{RESET}")
            dead_links.append((link, title))

    return live_links, dead_links, other_status


if __name__ == '__main__':
    main()
