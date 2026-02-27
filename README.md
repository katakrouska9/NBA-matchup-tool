# 🏀 NBA Matchup History Tool

## 📝 About This Project
This is a personal hobby project designed to help me quickly evaluate NBA matchups. The script fetches live games happening today and allows me to select a specific matchup to see how those two teams have performed against each other historically.

## 📂 Project Logic
The script follows a three-step logic:
* **Live Scoreboard:** Fetches real-time game statuses (Live, Final, or Start Time) using the NBA's live API endpoints.
* **Personalization:** Allows the user to pick a specific match from today's slate via the terminal.
* **Stats fetching**: It searches through thousands of games dating back to 2015, cleans the "Matchup" strings, maps team abbreviations to full names, and filters for only the games where these two specific teams met. It then returns the % of matches won.

## 🛠 Tech Stack
* **Data Source:** `nba_api` (Community-maintained NBA stats wrapper)