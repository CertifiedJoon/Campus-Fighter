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
### 여기에 move 이름 넣기! move이름은 folder이름과 같아야함.
moves = ["fall"]

TARGET_HEIGHT = 200  # Standard fighting game sprite height, adjust as needed
model_session = new_session("birefnet-general")


def process_images(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_folder, filename)
            # Save as PNG to preserve the transparent background
            output_path = os.path.join(
                output_folder, f"{os.path.splitext(filename)[0]}.png"
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
    for move_name in moves:
        output_folder = "sprites/keyboard/processed/" + move_name
        input_folder = "sprites/keyboard/raw/" + move_name
        os.makedirs(output_folder, exist_ok=True)
        process_images(input_folder, output_folder)
    print("Finished processing all images.")
