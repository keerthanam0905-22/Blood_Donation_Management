import pandas as pd
from datetime import datetime

# ==============================
# FILE PATHS (SET THESE)
# ==============================
STOCK_FILE_PATH = r"C:\Users\Shravani\Documents\stock.xlsx"
REQUEST_FILE_PATH = r"C:\Users\Shravani\Documents\requests.xlsx"

# ==============================
# COLORS
# ==============================
RED = "\033[91m"
ORANGE = "\033[93m"
YELLOW = "\033[33m"
GREEN = "\033[92m"
RESET = "\033[0m"

# ==============================
# BLOOD COMPATIBILITY
# ==============================
COMPATIBILITY = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"]
}

# ==============================
# EMERGENCY REQUEST SYSTEM
# ==============================
def emergency_request():

    print("\n===== Emergency Request System =====")

    patient_name = input("Enter Patient Name: ")
    blood_group = input("Enter Required Blood Group: ")
    pints_needed = int(input("Enter Number of Pints Needed: "))

    print("\nUrgency Level:")
    print("1. Urgent")
    print("2. Medium")
    print("3. Normal")

    urgency_level = int(input("Enter choice: "))

    if urgency_level == 1:
        color = RED
    elif urgency_level == 2:
        color = ORANGE
    else:
        color = YELLOW

    # Show Compatible Groups
    print("\nCompatible Blood Groups:")
    print(", ".join(COMPATIBILITY[blood_group]))

    # Load Stock
    stock_df = pd.read_excel(STOCK_FILE_PATH)

    stock_row = stock_df[stock_df["blood_group"] == blood_group]

    if not stock_row.empty:
        available = int(stock_row["pints"].values[0])

        if available >= pints_needed:
            # Provide blood
            stock_df.loc[
                stock_df["blood_group"] == blood_group,
                "pints"
            ] -= pints_needed

            stock_df.to_excel(STOCK_FILE_PATH, index=False)

            status = "Completed"
            print(GREEN + "\nBlood Provided Successfully." + RESET)

        else:
            status = "Waiting"
            print(color + "\nInsufficient Stock. Added to Waiting List." + RESET)
    else:
        status = "Waiting"
        print(color + "\nBlood Group Not Found. Added to Waiting List." + RESET)

    # Load or Create Request File
    try:
        request_df = pd.read_excel(REQUEST_FILE_PATH)
    except FileNotFoundError:
        request_df = pd.DataFrame(columns=[
            "request_id", "patient_name", "blood_group",
            "pints", "urgency_level", "request_time", "status"
        ])

    # Store request
    new_request = {
        "request_id": len(request_df) + 1,
        "patient_name": patient_name,
        "blood_group": blood_group,
        "pints": pints_needed,
        "urgency_level": urgency_level,
        "request_time": datetime.now(),
        "status": status
    }

    request_df = pd.concat([request_df, pd.DataFrame([new_request])], ignore_index=True)
    request_df.to_excel(REQUEST_FILE_PATH, index=False)

    print("Request Stored Successfully.\n")


# ==============================
# PRIORITY ALLOCATION FUNCTION
# ==============================
def allocate_to_waiting_list(blood_group, new_pints):

    print("\nProcessing Waiting List Allocation...")

    stock_df = pd.read_excel(STOCK_FILE_PATH)
    request_df = pd.read_excel(REQUEST_FILE_PATH)

    # Add new stock
    stock_df.loc[
        stock_df["blood_group"] == blood_group,
        "pints"
    ] += new_pints

    # Filter waiting patients for that group
    waiting = request_df[
        (request_df["blood_group"] == blood_group) &
        (request_df["status"] == "Waiting")
    ]

    if waiting.empty:
        print("No patients waiting.")
        stock_df.to_excel(STOCK_FILE_PATH, index=False)
        return

    waiting["request_time"] = pd.to_datetime(waiting["request_time"])

    # Sort by urgency first, then time
    waiting_sorted = waiting.sort_values(
        by=["urgency_level", "request_time"]
    )

    available = int(
        stock_df.loc[
            stock_df["blood_group"] == blood_group,
            "pints"
        ].values[0]
    )

    for _, row in waiting_sorted.iterrows():

        if available >= row["pints"]:
            available -= row["pints"]

            request_df.loc[
                request_df["request_id"] == row["request_id"],
                "status"
            ] = "Completed"

            print(GREEN + f"Allocated to {row['patient_name']}" + RESET)

        else:
            break

    stock_df.loc[
        stock_df["blood_group"] == blood_group,
        "pints"
    ] = available

    stock_df.to_excel(STOCK_FILE_PATH, index=False)
    request_df.to_excel(REQUEST_FILE_PATH, index=False)

    print("Waiting List Updated Successfully.\n")