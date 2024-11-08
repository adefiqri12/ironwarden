from PIL import Image

def png_to_ico_with_multiple_sizes(png_file_path, ico_file_path):
    try:
        # Open the PNG image
        with Image.open(png_file_path) as img:
            # Define a list of sizes you want in the ICO file
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
            
            # Create a list of resized images
            img_resized_list = [img.resize(size, Image.LANCZOS) for size in sizes]
            
            # Save as an ICO file with multiple sizes
            img.save(ico_file_path, format='ICO', sizes=sizes)
        print(f"ICO file with multiple sizes saved as {ico_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
png_file_path = 'ironwarden.png' 
ico_file_path = 'ironwarden.ico'
png_to_ico_with_multiple_sizes(png_file_path, ico_file_path)