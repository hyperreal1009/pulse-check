from bs4 import BeautifulSoup
import requests
import copy
import argparse
import random

def read_bookmarks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    bookmarks = [(a['href'], a.get_text())
                 for a in soup.find_all('a', href=True)]
    return bookmarks, soup

YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
PURPLE = '\033[95m'
RESET = '\033[0m'

def archive_dead_links(dead_links):
    with open('dead_links.html', 'w', encoding='utf-8') as f:
        f.write('<html><body>\n')
        for link, title in dead_links:
            f.write(f'<a href="{link}">{title}</a><br>\n')
        f.write('</body></html>\n')

def archive_other_status(other_status):
    with open('ignored.html', 'w', encoding='utf-8') as f:
        f.write('<html><body>\n')
        for link, title, status_code in other_status:
            f.write(f'<a href="{link}" data-status="{status_code}">{title}</a><br>\n')
        f.write('</body></html>\n')


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
    parser.add_argument('--purge', action='store_true', 
                        help='Remove invalid links and save a backup of the original file.')

    args = parser.parse_args()

    if args.smart_mode:
        timeout = random.randint(5, 10)
    else:
        timeout = args.timeout

    bookmarks, original_soup = read_bookmarks(args.filename)
    
    if args.purge:
        import shutil
        shutil.copy2(args.filename, args.filename + '.bak')  # Create a backup
        print(f"{YELLOW}[BACKUP]:{RESET} Backup created as {args.filename}.bak")
        
        purged_soup = filter_invalid_links(original_soup)
        with open(args.filename, 'w', encoding='utf-8') as f:
            f.write(str(purged_soup))
        bookmarks = [(a['href'], a.get_text())
                     for a in purged_soup.find_all('a', href=True)]
        
        print(f"{GREEN}[SUCCESS]:{RESET} Purged and saved cleaned data.")
       
        
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

def filter_invalid_links(soup):
    purged_soup = copy.deepcopy(soup)
    invalid_count = 0
    
    for a_tag in purged_soup.find_all('a', href=True):
        link = a_tag['href']
        if not (link.startswith('http://') or link.startswith('https://')):
            print(f"{YELLOW}[PURGING]:{RESET} Removing invalid link {PURPLE}{link}{RESET}")
            a_tag.extract()
            invalid_count += 1

    print(f"{YELLOW}[PURGED]:{RESET} {invalid_count} invalid links removed.")
    return purged_soup

def check_links(bookmarks, timeout, verbose, total_links):
    dead_links = []
    live_links = []
    other_status = []

    for idx, (link, title) in enumerate(bookmarks, start=1):
        if verbose:
            print(
                f"{YELLOW}[CHECKING {idx}/{total_links}]: {PURPLE}{title}{RESET} \n {link}")
        else:
            print(f"{YELLOW}[CHECKING]:{RESET} {idx}/{total_links} bookmarks...")

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
