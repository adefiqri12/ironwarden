import json

# Your JSON data (can also be loaded from a file or API)
data = {}

# Extract the 'animals' data
scraped_data = data.get("animals", [])

clean_text = "\n".join(scraped_data)

# Write the resulting animals data to a .txt file
with open('/unrelated_script/output.txt', 'w') as file:
    file.write(clean_text)

print("Animal data has been written to animals.txt")