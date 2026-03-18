import os

# 1. Define your custom download path
custom_model_path = "./my_custom_models"  # Or an absolute path like "C:/AI_Models/"

# Create the directory if it doesn't exist
os.makedirs(custom_model_path, exist_ok=True)

# 2. Set the environment variable
os.environ["U2NET_HOME"] = custom_model_path
from rembg import remove, new_session
from PIL import Image

# Configuration
print("input move name (should align with input folder name)")
move_name = input()
OUTPUT_FOLDER = "GameDesign/keyboard/processed/" + move_name
INPUT_FOLDER = "GameDesign/keyboard/raw/" + move_name
TARGET_HEIGHT = 200  # Standard fighting game sprite height, adjust as needed

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
model_session = new_session("birefnet-general")


def process_images():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(INPUT_FOLDER, filename)
            # Save as PNG to preserve the transparent background
            output_path = os.path.join(
                OUTPUT_FOLDER, f"{os.path.splitext(filename)[0]}.png"
            )
            if os.path.exists(output_path):
                pass

            try:
                with Image.open(input_path) as img:
                    # Remove the background
                    output_img = remove(img, session=model_session)

                    # Calculate new width to maintain aspect ratio
                    aspect_ratio = output_img.width / output_img.height
                    target_width = int(TARGET_HEIGHT * aspect_ratio)

                    # Resize the image
                    resized_img = output_img.resize(
                        (target_width, TARGET_HEIGHT), Image.Resampling.LANCZOS
                    )

                    resized_img.save(output_path, "PNG")
                    print(f"Successfully processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    print("Starting batch processing...")
    process_images()
    print("Finished processing all images.")
