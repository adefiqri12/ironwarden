file_path = 'dictionary\english_nouns.txt'
with open(file_path, 'r') as file:
    words = file.read().splitlines()

unique_words = set()
cleaned_words = []

for word in words:
    if word.isdigit():
        continue
    if word not in unique_words:
        unique_words.add(word)
        cleaned_words.append(word)

output_file = 'dictionary\cleaned.txt'
with open(output_file, 'w') as file:
    for word in cleaned_words:
        file.write(word + '\n')

print(f'Duplicates removed and cleaned file saved as {output_file}')