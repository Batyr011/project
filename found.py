import sqlite3
from datetime import datetime

# Initialize Database
conn = sqlite3.connect("lost_found.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    location_found TEXT NOT NULL,
    date_found TEXT NOT NULL,
    claimed_status TEXT DEFAULT 'No'
)
""")
conn.commit()

# Function to report a found item
def report_item():
    name = input("Enter item name: ")
    category = input("Enter category: ")
    location = input("Enter location found: ")
    date_found = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("INSERT INTO items (item_name, category, location_found, date_found) VALUES (?, ?, ?, ?)",
                   (name, category, location, date_found))
    conn.commit()
    print("\nItem reported successfully!\n")

# Function to search for an item
def search_items():
    query = input("Enter item name, category, or location to search: ")
    cursor.execute("SELECT * FROM items WHERE (item_name LIKE ? OR category LIKE ? OR location_found LIKE ?) AND claimed_status = 'No'",
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()

    if results:
        print("\nLost Items Found:")
        for item in results:
            print(f"ID: {item[0]} | Name: {item[1]} | Category: {item[2]} | Location: {item[3]} | Date Found: {item[4]}")
    else:
        print("\nNo matching items found.\n")

# Function to view all unclaimed items
def view_unclaimed_items():
    cursor.execute("SELECT * FROM items WHERE claimed_status = 'No'")
    items = cursor.fetchall()

    if items:
        print("\nUnclaimed Items:")
        for item in items:
            print(f"ID: {item[0]} | Name: {item[1]} | Category: {item[2]} | Location: {item[3]} | Date Found: {item[4]}")
    else:
        print("\nNo unclaimed items available.\n")

# Function to claim an item
def claim_item():
    item_id = input("Enter the ID of the item to claim: ")
    cursor.execute("SELECT * FROM items WHERE item_id = ? AND claimed_status = 'No'", (item_id,))
    item = cursor.fetchone()

    if item:
        cursor.execute("UPDATE items SET claimed_status = 'Yes' WHERE item_id = ?", (item_id,))
        conn.commit()
        print("\nItem successfully claimed!\n")
    else:
        print("\nItem not found or already claimed.\n")

# Simple menu
def menu():
    while True:
        print("\n--- Lost & Found System ---")
        print("1. Report a Found Item")
        print("2. Search for a Lost Item")
        print("3. View All Unclaimed Items")
        print("4. Claim an Item")
        print("5. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            report_item()
        elif choice == "2":
            search_items()
        elif choice == "3":
            view_unclaimed_items()
        elif choice == "4":
            claim_item()
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

# Run the menu
if __name__ == "__main__":
    menu()

# Close the database connection when done
conn.close()
