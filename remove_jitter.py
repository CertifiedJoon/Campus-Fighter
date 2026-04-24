from PIL import Image


def fix_mugen_borders(image_path, output_path, threshold=128):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # item[3] is the Alpha channel (0 to 255)
        if item[3] < threshold:
            # Make it 100% transparent
            new_data.append((0, 0, 0, 0))
        else:
            # Make it 100% opaque
            new_data.append((item[0], item[1], item[2], 255))

    img.putdata(new_data)
    img.save(output_path, "PNG")


# Run this on your intro frames specifically
if __name__ == "__main__":
    fix_mugen_borders(
        "Graduate.png",
        "Graduate_jitter_removed.png",
    )
