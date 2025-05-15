from modules import tracker, bankroll, odds_api

def main():
    while True:
        # Main menu
        print("\n" + "═"*50)
        print("        🎯 SPORTS BETTING ASSISTANT 🎯")
        print("═"*50)
        print("\n1. 🏆  Select sport and view live odds")
        print("2. 🚪  Exit")
        print("\n" + "═"*50)

        choice = input("\nSelect an option (1-2): ")
        if choice == "1":
            print("\n" + "━"*40)
            print("         AVAILABLE SPORTS")
            print("━"*40)
            print("\n1. ⚽  Soccer")
            print("\n" + "━"*40)

            sport_choice = input("\nSelect sport (1): ")

            if sport_choice != "1":
                print("\n❌ Only Soccer is supported currently.")
                continue

            from modules.odds_api import COUNTRY_LEAGUES

            print("\n" + "━"*40)
            print("        AVAILABLE COUNTRIES")
            print("━"*40)

            for idx, country in enumerate(COUNTRY_LEAGUES.keys(), 1):
                print(f"{idx}. 🌍  {country}")

            country_choice = input("\nSelect country (1-6): ")

            try:
                country_index = int(country_choice) - 1
                selected_country = list(COUNTRY_LEAGUES.keys())[country_index]
                sport_key = COUNTRY_LEAGUES[selected_country]
                sport_name = f"Soccer - {selected_country}"
            except (ValueError, IndexError):
                print("\n❌ Invalid country choice!")
                continue

            print(f"\n📊 Fetching live odds for {sport_name}...")
            matches = odds_api.fetch_odds(sport_key)

            if matches:
                pass  # fetch_odds handles match display and detail selection internally
        
        elif choice == "2":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option!")

if __name__ == "__main__":
    main()