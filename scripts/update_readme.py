import os
import re
from datetime import datetime, timezone, timedelta
from github import Github
import sys

# Configurazione
README_PATH = 'README.md'
REPO_LIST_REGEX = r'\[([^\]]+)\]\((https://github\.com/[^)]+)\)'
SPECIAL_CHAR = '⭐'  # Carattere speciale da aggiungere
TIMEZONE_OFFSET = timedelta(hours=1)  # CET = UTC+1, CEST = UTC+2 (puoi migliorare gestendo l'ora legale)

def get_current_time():
    utc_now = datetime.now(timezone.utc)
    local_now = utc_now + TIMEZONE_OFFSET
    return local_now.strftime("%d/%m/%Y at %H:%M")

def main():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("GITHUB_TOKEN not found in environment variables.", file=sys.stderr)
        sys.exit(1)
    
    try:
        g = Github(token)
    except Exception as e:
        print(f"Error authenticating with GitHub: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            readme = f.read()
    except FileNotFoundError:
        print(f"{README_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    matches = re.findall(REPO_LIST_REGEX, readme)
    updated_readme = readme

    for name, url in matches:
        try:
            repo = g.get_repo(url.replace('https://github.com/', ''))
        except Exception as e:
            print(f"Error accessing repository {url}: {e}", file=sys.stderr)
            continue

        commits = repo.get_commits(since=datetime.utcnow() - timedelta(days=1))
        file_changes = 0
        last_update = None

        for commit in commits:
            stats = commit.stats
            file_changes += len(commit.files)  # Conta il numero di file modificati
            if not last_update:
                last_update = commit.commit.author.date

        # Verifica se ci sono più di 5 file modificati
        if file_changes > 5:
            special = f' {SPECIAL_CHAR}'
        else:
            special = ''

        if last_update:
            local_update = last_update + TIMEZONE_OFFSET
            update_str = f"Last update {local_update.strftime('%d/%m/%Y')} at {local_update.strftime('%H:%M')}"
        else:
            update_str = "No recent updates"

        # Crea una nuova stringa per sostituire
        pattern = re.escape(f'[{name}]({url})')
        replacement = f'[{name}]({url}){special} - {update_str}'

        # Usa regex per sostituire solo la prima occorrenza
        updated_readme = re.sub(pattern, replacement, updated_readme, count=1)

    # Scrivi il README aggiornato
    try:
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_readme)
    except Exception as e:
        print(f"Error writing to {README_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
