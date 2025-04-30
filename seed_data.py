import sqlite3

DATABASE_PATH = "database/database.db"

sample_data = [
    ("Green Leaf Café", "Campus North", "Vegan", "Gluten-Free", "Fresh local vegan meals."),
    ("Burger Bliss", "Campus South", "American", "None", "All-American burgers and fries."),
    ("Sushi World", "Downtown", "Japanese", "Vegetarian", "Sushi and bento for all diets.")
]

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

cursor.executemany("""
    INSERT INTO dining_options (name, location, cuisine, dietary, description)
    VALUES (?, ?, ?, ?, ?)
""", sample_data)

connection.commit()
connection.close()

print("✅ Sample data inserted.")
