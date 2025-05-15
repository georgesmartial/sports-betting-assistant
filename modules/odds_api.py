import requests
from config import API_KEY, ODDS_API_URL
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

COUNTRY_LEAGUES = {
    "England": {
        "Premier League": "soccer_epl"
    },
    "France": {
        "Ligue 1": "soccer_france_ligue_one"
    },
    "Germany": {
        "Bundesliga": "soccer_germany_bundesliga",
        "2. Bundesliga": "soccer_germany_bundesliga2"
    },
    "Netherlands": {
        "Eredivisie": "soccer_netherlands_eredivisie"
    },
    "Portugal": {
        "Primeira Liga": "soccer_portugal_primeira_liga"
    },
    "Spain": {
        "La Liga": "soccer_spain_la_liga"
    }
}


def fetch_odds(sport_key, region="eu", market="h2h"):
    # --- API Connection
    if isinstance(sport_key, dict):
        sport_key = next(iter(sport_key.values()))
    elif isinstance(sport_key, set):
        sport_key = next(iter(sport_key))
    elif isinstance(sport_key, str):
        sport_key = sport_key.replace('v4/sports/', '')

    print("\n📡 Connecting to API...")
    print(f"Sport key: {sport_key}")

    base_url = ODDS_API_URL.rstrip('/')
    url = f"{base_url}/{sport_key}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": region,
        "markets": market,
        "bookmakers": "pinnacle"
    }

    try:
        print("\n🔍 Fetching odds...")
        response = requests.get(url, params=params)
        debug_url = url + '?' + '&'.join(f"{k}={v}" for k, v in params.items() if k != 'apiKey')
        print(f"Debug: Requesting URL: {debug_url}")

        if response.status_code != 200:
            print(f"❌ API Error: Status code {response.status_code}")
            print(f"URL attempted: {response.url}")
            return []

        odds_data = response.json()
        print(f"✅ Successfully received {len(odds_data)} matches from API")

        if not odds_data:
            print("❌ Error: Empty response from API")
            return []

        if isinstance(odds_data, dict) and 'message' in odds_data:
            print(f"❌ API Error: {odds_data['message']}")
            return []

        # --- Timezone Setup
        local_tz = ZoneInfo("Europe/Berlin")
        matches = []

        # --- Match Filtering
        for match in odds_data:
            try:
                utc_time = datetime.fromisoformat(match['commence_time'].replace("Z", "+00:00"))
                local_time = utc_time.astimezone(local_tz)

                matches.append({
                    "home_team": match.get("home_team", "Unknown"),
                    "away_team": match.get("away_team", "Unknown"),
                    "commence_time": local_time,
                    "bookmakers": match.get("bookmakers", [])
                })
            except KeyError as e:
                print(f"❌ Debug: Missing key in match data: {e}")
                continue

        matches.sort(key=lambda x: x['commence_time'])
        next_ten_matches = matches[:10]

        # --- Display Matches
        print("\n📅 Next up to 10 matches:")
        print("═" * 60)
        for idx, match in enumerate(next_ten_matches, 1):
            print(f"{idx}. 🏟️  {match['home_team']} vs {match['away_team']}")
            print(f"   ⏰  {match['commence_time'].strftime('%A, %d %B %Y at %H:%M')}")
            print("─" * 60)

        # --- User Selection and Details
        selection = input("\nSelect a match number for details (or press Enter to skip): ")
        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(next_ten_matches):
                selected_match = next_ten_matches[index]
                print("\n" + "═" * 60)
                print(f"Match: {selected_match['home_team']} vs {selected_match['away_team']}")
                print(f"Date & Time: {selected_match['commence_time'].strftime('%A, %d %B %Y at %H:%M')}")
                print("═" * 60)

                h2h_odds = {}
                totals_odds = {}
                for bookmaker in selected_match['bookmakers']:
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'h2h':
                            for outcome in market['outcomes']:
                                h2h_odds[outcome['name']] = outcome['price']
                        elif market['key'] == 'totals':
                            for outcome in market['outcomes']:
                                totals_odds[outcome['name']] = outcome['price']

                print("\n📊 Betting Odds:")
                if h2h_odds:
                    print("\nHead-to-Head (h2h):")
                    for team, price in h2h_odds.items():
                        print(f"  • {team}: {price}")
                else:
                    print("\n❌ No h2h odds available.")

                if totals_odds:
                    print("\nTotals:")
                    for outcome, price in totals_odds.items():
                        print(f"  • {outcome}: {price}")
                else:
                    print("\n❌ No totals odds available.")

                print("\n📈 Betting Advice:")
                if h2h_odds:
                    home_team = selected_match['home_team']
                    away_team = selected_match['away_team']
                    home_price = h2h_odds.get(home_team, float('inf'))
                    away_price = h2h_odds.get(away_team, float('inf'))

                    if home_price < away_price:
                        print(f"  🏠 Bet on {home_team} to win (lower odds: {home_price})")
                    elif away_price < home_price:
                        print(f"  🛫 Bet on {away_team} to win (lower odds: {away_price})")
                    else:
                        print("  🤔 No clear favorite for h2h.")

                if totals_odds:
                    over_price = totals_odds.get("Over 2.5", float('inf'))
                    under_price = totals_odds.get("Under 2.5", float('inf'))

                    if over_price < under_price:
                        print(f"  📈 Bet on Over 2.5 goals (lower odds: {over_price})")
                    elif under_price < over_price:
                        print(f"  📉 Bet on Under 2.5 goals (lower odds: {under_price})")
                    else:
                        print("  🤔 No clear favorite for totals.")
            else:
                print("\n❌ Invalid match selection!")
        else:
            print("\n❌ Please enter a valid number!")

        return next_ten_matches

    except Exception as e:
        print(f"❌ Error fetching odds: {e}")
        print(f"Debug: Full error details: {repr(e)}")
        return []