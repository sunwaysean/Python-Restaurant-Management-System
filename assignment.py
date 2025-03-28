import random
import datetime

# divider = "----------------------------------------------------------------------"

def displayMenu():
    with open('menu.txt', 'r') as f: 
        for line in f:
            print(line)

def displayReservation():
    # Table headers
    headers = ["Date", "Slot", "Name", "Email", "ID", "Order"]
    # Format string for table row
    row_format = "{:<12} {:<8} {:<15} {:<25} {:<10} {:<5}"

    # Print table headers
    print(row_format.format(*headers))
    print("-" * 100)

    # Open the file and read reservations
    with open('reservation.txt', 'r') as file:
        reservations = file.readlines()

    # Print each reservation
    for reservation in reservations:
        # Remove leading/trailing whitespaces and split the fields
        fields = reservation.strip().split('|')
        # Print formatted row
        print(row_format.format(*fields))

def mealRecommendation():
    menu = open('menu.txt').read().splitlines()
    print("Chef's recommendation: "+random.choice(menu))
    #try to make it print more than 1 recommendation (generate from list? do later)

def addReservation():
    # Prompt the user for reservation information
    while True:
        try:
            month = int(input("Enter the month (1-12): "))
            day = int(input("Enter the day (1-31): "))
            input_date = datetime.datetime(datetime.datetime.now().year, month, day).date()
            today = datetime.datetime.now().date()
            if input_date >= today + datetime.timedelta(days=5):
                date = input_date.strftime("%Y-%m-%d")
            else:
                print("Error: Please enter a date that is more than 5 days from today.")
                break
        except ValueError:
            print("Invalid input. Please enter valid month and day.")
            break

        try:
            slot = int(input("Please select a time slot:\n1. 12:00 pm - 02:00 pm\n2. 02:00 pm - 04:00 pm\n3. 06:00 pm - 08:00 pm\n4. 08:00 pm - 10:00 pm\nEnter your choice (1-4): "))
            if 1 <= slot <= 4:
                if slot == 1:
                    slot1 = "12:00 pm - 02:00 pm"
                elif slot == 2:
                    slot1 = "02:00 pm - 04:00 pm"
                elif slot == 3:
                    slot1 = "06:00 pm - 08:00 pm"
                elif slot == 4:
                    slot1 = "08:00 pm - 10:00 pm"
            else:
                print("Invalid selection. Please try again.")
                break
        except ValueError:
                print("Invalid input. Please enter a number.")
                break
        
        name = input("Enter name: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        
        try:
            pax = input("Enter the pax number: ")
            if int(pax) >= 5:
                print("Maximum 4 pax allowed")
                break
        except ValueError:
                print("Invalid input. Please enter a number.")
                break
        with open('reservation.txt', 'r') as file:
            reservations = file.readlines()

        matching_reservations = [r for r in reservations if r.startswith(date + '|' + slot1)]

        if len(matching_reservations) < 8:
            number = len(matching_reservations) + 1
            reservation = f"{date}|{slot1}|{name}|{email}|{phone}|{pax}|{number}\n"
            with open('reservation.txt', 'a') as file:
                file.write(reservation)
            print("Reservation added successfully!\n")
        else:
            print("Error: This date and time slot is full. Maximum of 8 reservations allowed.\n")
        break
    
    try:
        another = input("Would you like to make another reservation? (y/n)")
        if another == "y":
            addReservation()
        elif another == "n":
            pass
    except ValueError:
            print("Invalid input. Please enter y or n.")

def main():
    while True:
        print("----------------------------------------------------------------------\n\n=============================\n=        Main Menu          =\n=============================")
        print("0. Quit\n1. Display Reservations\n2. Display Menu\n3. Add Reserveation\n4. Delete Reservation\n5. Generate Recommendations")
        selection = int(input("Your Selection: "))
        match selection:
            case 0:
                break
            case 1:
                displayReservation()
            case 2:
                displayMenu()
            case 3:
                addReservation()
            # case 4:
            #     delReservation()
            case 5:
                mealRecommendation()
            case default:
                print("Invalid selection!")


if __name__ == "__main__":
    main()

