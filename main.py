from modules import tracker, bankroll

def main():
    while True:
        print("\n--- Sports Betting Assistant ---")
        print("1. View bankroll")
        print("2. Add a bet")
        print("3. Predict match outcome")
        print("4. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            bankroll.view_bankroll()
        elif choice == "2":
            tracker.add_bet()
        elif choice == "3":
            print("Prediction engine coming soon...")
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()