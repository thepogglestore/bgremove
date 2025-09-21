from rembg import remove
from PIL import Image
from io import BytesIO
import os

# Settings
input_folder = 'output'
output_folder = 'output_images'
final_size = (1000, 1000)
target_height = 900  # Desired object height after background removal

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process all images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)

        # Step 1: Remove background
        with open(input_path, 'rb') as i:
            output_data = i.read()
            

        # Step 2: Open transparent image
        img = Image.open(BytesIO(output_data)).convert('RGBA')

        # Step 3: Crop transparent areas tightly
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)

        # Step 4: Resize to target height, keep aspect ratio
        aspect_ratio = img.width / img.height
        new_width = int(target_height * aspect_ratio)
        img = img.resize((new_width, target_height), Image.LANCZOS)


        # Step 5: Create white background canvas
        background = Image.new('RGB', final_size, (255, 255, 255))

        # Step 6: Center the resized object
        offset = (
            (final_size[0] - new_width) // 2,
            (final_size[1] - target_height) // 2
        )
        background.paste(img, offset, img)

        # Step 7: Save final image
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + 'black.jpg')
        background.save(output_path, 'JPEG', quality=95)

        print(f"✅ Processed: {filename}")

print("\n🎉 All images processed successfully without stretching!")
