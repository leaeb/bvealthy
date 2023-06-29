import requests
import json
import sqlite3

def download_vegan_products():
    url = "https://de.openfoodfacts.org/label/vegan"
    params = {
        "action": "process",
        "tagtype_0": "ingredients",
        #"tag_contains_0": "en:vegan",
        "page_size": 100,
        "json": "true"
    }

    all_products = []

    page = 1
    while True:
        params["page"] = page
        print("Sending GET-Request")
        response = requests.get(url, params=params)
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            break

        if not data.get("products"):
            break
        if page>1:
            break

        all_products.extend(data["products"])
        page += 1

    return all_products


def create_database(products):
    print("Connecting Database")

    conn = sqlite3.connect("vegan_products.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id TEXT, name TEXT, brand TEXT, ingredients TEXT, quantity TEXT, last_modified TEXT, labels TEXT, image_small_url TEXT, nova_group TEXT, energy_100g TEXT, nutrition_grade TEXT)''')

    for product in products:
        id = product.get("code")
        name = product.get("product_name")
        brand = product.get("brands")
        ingredients = product.get("ingredients_text")
        quantity = product.get("quantity")
        last_modified = product.get("last_modified_t")
        labels = product.get("labels")
        image_small_url = product.get("image_small_url")
        nova_group = product.get("nova_group")
        energy_100g = product.get("energy_100g")
        nutrition_grade = product.get("nutrition_grades")

        c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, name, brand, ingredients,quantity, last_modified,labels,image_small_url,nova_group,energy_100g,nutrition_grade))

    conn.commit()
    conn.close()

# do:
products = download_vegan_products()
create_database(products)
print("Anzahl der veganen Produkte, die in Deutschland erhältlich sind:", len(products))
print("Datenbank wurde erfolgreich erstellt.")
