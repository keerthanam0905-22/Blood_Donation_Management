from openpyxl import load_workbook

filename = "stock.xlsx"
LOW_STOCK_LIMIT = 5   # Alert if units <= 5





def display_stock():
    workbook = load_workbook(filename)
    sheet = workbook.active

    print("\n📊 Display Options:")
    print("1. Display All Blood Groups")
    print("2. Display Specific Blood Group")

    choice = input("Enter choice: ")

    # DISPLAY ALL
    if choice == "1":
        print("\n📋 All Blood Stock:")
        print("----------------------------")

        for row in sheet.iter_rows(min_row=2, values_only=True):
            blood_group = row[0]
            units = row[1]

            print(f"{blood_group} : {units} units")

            if units <= LOW_STOCK_LIMIT:
                print(f"⚠ ALERT: Low stock for {blood_group}")

        print("----------------------------\n")

    # DISPLAY SPECIFIC
    elif choice == "2":
        blood = input("Enter Blood Group: ").upper()

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] == blood:
                units = row[1]

                print("\n🔎 Blood Group Details")
                print("----------------------------")
                print(f"{blood} : {units} units")

                if units <= LOW_STOCK_LIMIT:
                    print(f"⚠ ALERT: Low stock for {blood}")

                print("----------------------------\n")
                return

        print("❌ Blood group not found!")

    else:
        print("Invalid choice!")
display_stock()
  