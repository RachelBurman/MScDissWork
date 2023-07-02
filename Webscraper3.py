import requests
from bs4 import BeautifulSoup

search_string = "Almond Meal"
base_url = "https://www.allrecipes.com/search/results/?search="

page_number = 1
total_pages = 1

while page_number <= total_pages:

    # Construct the URL for the current page
    url = base_url + search_string + "&page=" + str(page_number)

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the total number of pages
    if page_number == 1:
        pagination = soup.find("ul", class_="pagination")
        if pagination:
            total_pages = len(pagination.find_all("li")) - 2

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

       # print("-------------------")

    # Move to the next page
    page_number += 1
