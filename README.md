# When will the code be released?  
- [SynthLight: Portrait Relighting with Diffusion Model by Learning to Re-render Synthetic Faces](https://vrroom.github.io/synthlight/)
- [FramePainter: Endowing Interactive Image Editing with Video Diffusion Priors](https://github.com/YBYBZhang/FramePainter)
- [1-2-1: Renaissance of Single-Network Paradigm for Virtual Try-On](https://github.com/ningshuliang/1-2-1-MNVTON)
- [Token Verse](https://token-verse.github.io/)
- [Wonderland: Navigating 3D Scenes from a Single Image](https://snap-research.github.io/wonderland/)
- [Enhancing Real-World Video Super-Resolution with Diffusion Models](https://github.com/xh9998/DiffVSR-project)
  

--------------- 

## This repository keep track when the code will be release 

Tired of checking all the repositories for the papers I was interested in, I created this repository that does the daily checking for me. It checks when the code is released and updates the Readme file with the update information.

***In this repository I keep track of the most interesting Papers about Text to Image generative field.***

# Main Steps:
**Workflow Triggers:** The workflow is scheduled to run every day at 12:00 PM Italian time using a cron expression.

**Time Zone Settings:** Since GitHub Actions uses UTC time, we calculated the Italian time zone (CET/CEST) to correctly schedule the execution at 12:00.

**Repository Checkout:** We use the actions/checkout action to access the repository content, including README files.
Running a Python Script: A simple Python script does the following:
- Reads the README.md file.
- Extracts links to the GitHub repositories.
- For each repository, checks the latest commits to see if there are updates with more than 5 files changed.
- Adds a special character if the condition is met.
- Updates the README with the time of the last update.
- Commits and Pushes Changes: If the script makes changes to the README, they are committed and pushed to the repository.

## Python script
**Repository Extraction:** Uses a regex to extract all GitHub repository links in the README.

**Authentication with GitHub:** Uses the GITHUB_TOKEN provided by the action to authenticate and access the GitHub API.

**Check for Updates:**
- Fetches commits from the last 24 hours.
- Counts file additions and deletions to estimate if there were more than 5 changes.
- Logs the last update.

**README Update:**
- Adds a special character (⭐) next to the repository link if the condition is met.
- Adds the string "Last update dd/mm/yyyy at hh:mm" next to the repository link.
- Time Zone Handling: Considers an offset of +1 hour for Italian time zone. You can improve the script to automatically handle daylight saving time.


***Time Zone Handling: The current implementation uses a fixed offset of +1 hour. For more accurate DST handling, you can use libraries like pytz or zoneinfo (for Python 3.9+) to automatically determine the Italian time zone.***
````
from zoneinfo import ZoneInfo

def get_current_time():
    now = datetime.now(ZoneInfo("Europe/Rome"))
    return now.strftime("%d/%m/%Y at %H:%M")

````
