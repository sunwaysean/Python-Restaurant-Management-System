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

        slot1 = none

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

def read_reservations():
    reservation_list = []
    try:
        with open('reservation.txt', "r") as file:
            for line in file:
                reservation = line.strip().split("|")
                reservation_list.append(reservation)
    except FileNotFoundError:
        pass
    return reservation_list

def editReservation():
    print("==== Update/Edit Reservation ====")
    name = input("Enter the name of the reservation to update: ").lower()

    # Mapping slot number to time slot
    slot_mapping = {
        '1': "12:00 pm - 02:00 pm",
        '2': "02:00 pm - 04:00 pm",
        '3': "06:00 pm - 08:00 pm",
        '4': "08:00 pm - 10:00 pm"
    }

    while True:
        slot_input = input("Enter the slot number (1, 2, 3, or 4) of the reservation to update: ")
        slot1 = slot_mapping.get(slot_input)
        if slot1:
            break
        else:
            print("Invalid slot number. Please enter a valid slot number (1, 2, 3, or 4).")

    # Read existing reservations from the file
    with open('reservation.txt', 'r') as file:
        reservations = file.readlines()

    updated = False

    with open('reservation.txt', 'w') as file:
        for reservation in reservations:
            fields = reservation.strip().split('|')
            if fields[2].lower() == name and fields[1].lower() == slot1:
                updated = True
                print(f"Current reservation: {reservation}")
                
                new_date = input("Enter the new date (YYYY-MM-DD) [Leave blank to keep the current value]: ")
                
                new_session = input("Enter the new session (1, 2, 3, or 4) [Leave blank to keep the current value]: ")
               
                new_pax = input("Enter the new number of people [Leave blank to keep the current value]: ")
                if new_pax:
                    if int(new_pax) > 4:
                        print("Error: Number of people cannot exceed 4. The reservation will not be updated.")
                        reservations.append(reservation)  # Add the current reservation back to the list
                        continue  # Skip updating and move to the next reservation
                
                new_phone = input("Enter the new phone number [Leave blank to keep the current value]: ")
                if not new_phone.startswith("01") or len(new_phone) != 10:
                    print("Error: Invalid phone number format. The reservation will not be updated.")
                    reservations.append(reservation)  # Add the current reservation back to the list
                    continue  # Skip updating and move to the next reservation
                
                new_email = input("Enter the new email [Leave blank to keep the current value]: ")
                if new_email:
                    if "@" not in new_email or ".com" not in new_email:
                        print("Error: Invalid email format. The reservation will not be updated.")
                        reservations.append(reservation)  # Add the current reservation back to the list
                        continue  # Skip updating and move to the next reservation
                
                new_slot = slot_mapping.get(new_session)
                if not new_slot:
                    new_slot = fields[1]

                 # Check if the number of reservations on the new date is less than 32
                if new_date:
                    count_reservations_on_new_date = sum(1 for r in reservations if r.startswith(new_date))
                    if count_reservations_on_new_date >= 32:
                        print(f"Error: The date {new_date} is fully booked. Please choose another date.")
                        return

                # Check if the number of reservations on the new slot is less than 8
                if new_slot:
                    count_reservations_on_new_slot = sum(1 for r in reservations if r.split('|')[1] == new_slot)
                    if count_reservations_on_new_slot >= 8:
                        print(f"Error: The slot {new_slot} is fully booked. The reservation will not be updated.")
                        reservations.append(reservation)  # Add the current reservation back to the list
                        continue  # Skip updating and move to the next reservation
                        
                    
                    fields[0] = new_date or fields[0]
                    fields[1] = new_slot or fields[1]
                    fields[4] = new_phone or fields[4]
                    fields[3] = new_email or fields[3]
                    fields[5] = new_pax or fields[5]

                    updated_reservation = '|'.join(fields)
                    print(f"Updated reservation: {updated_reservation}")
                    file.write(updated_reservation + "\n")
            else:
                file.write(reservation)

    if not updated:
        print("No reservations found with the given name, slot, and date.")

    another_edit = input("Would you like to edit another reservation? (y/n): ").lower()
    if another_edit == "y":
        editReservation()
    else:
        print("Reservation editing completed.")

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

