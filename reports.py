import pandas as pd
import matplotlib.pyplot as plt


# ==================================
# READ FILES SAFELY
# ==================================

def read_donors():
    df = pd.read_excel("donor.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def read_stock():
    df = pd.read_excel("stock.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def read_requests():
    df = pd.read_excel("requests.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


# ==================================
# 1️⃣ TOTAL DONORS
# ==================================

def total_donors():
    df = read_donors()
    return len(df)


# ==================================
# 2️⃣ BLOOD STOCK SUMMARY
# ==================================

def blood_stock_summary(threshold=5):
    df = read_stock()

    print("\n📊 Blood Stock Summary:")
    print(df)

    # Graph Representation
    plt.figure()
    plt.bar(df["blood_group"], df["units"])
    plt.title("Blood Stock Summary")
    plt.xlabel("Blood Group")
    plt.ylabel("Units Available")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Low Stock Alert
    low_stock = df[df["units"] < threshold]

    if not low_stock.empty:
        print("\n⚠ LOW STOCK ALERT (Below Threshold):")
        print(low_stock)
    else:
        print("\n✅ All blood groups are sufficiently stocked.")


# ==================================
# 3️⃣ MOST REQUESTED BLOOD GROUP
# ==================================

def most_requested_blood():
    df = read_requests()
    total_pints = df.groupby("blood_group")["pints_needed"].sum()
    sorted_pints = total_pints.sort_values(ascending=False)
    print("\n📊 Blood Demand Summary (By Total Pints Needed):")
    print(sorted_pints)
    top_group = sorted_pints.idxmax()
    top_value = sorted_pints.max()
    print(f"\n🩸 Most Requested Blood Group: {top_group} ({top_value} pints needed)")
    plt.figure()
    sorted_pints.plot(kind="bar")
    plt.title("Most Requested Blood Group (By Pints Needed)")
    plt.xlabel("Blood Group")
    plt.ylabel("Total Pints Needed")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ==================================
# 4️⃣ DONATION HISTORY
# ==================================

def donation_history():
    df = read_donors()

    # Convert LastDonation column safely (DD-MM-YYYY format)
    df["lastdonation"] = pd.to_datetime(
        df["lastdonation"],
        errors="coerce",
        dayfirst=True
    )

    # Sort by latest donation
    sorted_df = df.sort_values(by="lastdonation", ascending=False)

    print("\n📅 Donation History (Latest First):")
    print(sorted_df[["name", "blood", "lastdonation"]])

    # Pictorial Representation – Donor distribution by blood group
    donation_count = df["blood"].value_counts()

    plt.figure()
    donation_count.plot(kind="bar")
    plt.title("Donor Distribution by Blood Group")
    plt.xlabel("Blood Group")
    plt.ylabel("Number of Donors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ==================================
# MAIN FUNCTION
# ==================================

def main():

    print("\n========== BLOOD DONATION REPORT ==========\n")

    print("👥 Total Donors:", total_donors())

    blood_stock_summary(threshold=5)

    most_requested_blood()

    donation_history()


if __name__ == "__main__":
    main()