
import re
import requests
import os

## Welcome 
def validate_url(url):
    pattern = r"^https?://[A-Za-z0-9.-]+\.[a-z]{2,}/*$"
    return re.match(pattern, url)

def get_wordlist():
    user_input = input("Enter path to wordlist file (or press Enter to use default): ").strip()
    if user_input and os.path.exists(user_input):
        print(f"[+] Using custom wordlist: {user_input}")
        return user_input
    else:
        print("[*] Using default wordlist.")
        default_words = [
            "admin", "login", "uploads", "images", "config", "backup", 
            ".git", ".env", "_admin", "_private", "hidden", "server-status"
        ]
        default_file = "default_wordlist.txt"
        with open(default_file, "w") as f:
            f.write("\n".join(default_words))
        return default_file

def find_directories(url, wordlist_path):
    found_dirs = []
    with open(wordlist_path, "r") as f:
        for line in f:
            word = line.strip()
            test_url = f"{url.rstrip('/')}/{word}/"
            try:
                response = requests.get(test_url, timeout=5)
                if response.status_code in [200, 301, 302]:
                    print(f"[+] Found: {test_url} (Status: {response.status_code})")
                    found_dirs.append(test_url)
                elif response.status_code == 403:
                    print(f"[!] Forbidden: {test_url} (Potentially exists)")
                    found_dirs.append(test_url + " [403]")
            except requests.RequestException:
                print(f"[-] Failed: {test_url}")
                continue

    if found_dirs:
        with open("output.txt", "w") as out:
            for item in found_dirs:
                out.write(item + "\n")
        print("[*] Discovered directories saved to output.txt")
    else:
        print("[-] No directories found.")

if __name__ == "__main__":

    url = input("Enter a URL (http:// or https://): ").strip()

    if not validate_url(url):
        print("Invalid URL format. Must start with http:// or https:// and be a valid domain.")
    else:
        wordlist = get_wordlist()
        find_directories(url, wordlist)
