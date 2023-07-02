import requests
from bs4 import BeautifulSoup

search_string = "Almonds"
base_url = "https://www.allrecipes.com/search/"

page_number = 1
items_per_page = 24
has_next_page = True

while has_next_page:
    # Calculate the offset for the current page
    
    offset = (page_number - 1) * items_per_page
    
    # Construct the URL for the current page
    url = f"{base_url}?Almonds=Almonds&offset={offset}&q={search_string}"
   
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the recipe containers on the page
    recipe_containers = soup.find_all("article", class_="fixed-recipe-card")

    # Iterate through the recipe containers and extract information
    for recipe in recipe_containers:
        
        recipe_title = recipe.find("span", class_="fixed-recipe-card__title-link").text.strip()
        recipe_url = recipe.find("a", class_="fixed-recipe-card__title-link")["href"]

        # Get the details of the recipe
        response = requests.get(recipe_url)
        recipe_soup = BeautifulSoup(response.content, 'html.parser')

        # Extract recipe details such as servings and ingredients
        # ...

        # Display result:
        print("## %s:" % recipe_title)  # Name of the recipe
        print("### For %s servings:" % nb_servings)
        # Print other recipe details and steps

        print("-------------------")

    # Check if there is a "Next" button on the page
    next_button = soup.find("a", class_="next")
    has_next_page = next_button is not None

    # Move to the next page
    page_number += 1
