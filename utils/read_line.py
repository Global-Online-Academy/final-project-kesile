from PIL import Image

def read_line_chart(image_path):
    image = Image.open(image_path)
    width, height = image.size

    # set image contrast to max, so its only black and white, no gray at all
    image = image.convert('L')
    image = image.point(lambda x: 255 if x > 150 else 0)
    # iterate through x and read each y position of each black pixel
    y_pos = []
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) == 0:
                y_pos.append(y)
                break
    y_pos = [round(y / height * 100) for y in y_pos]
    y_pos = [100 - y for y in y_pos]
    return y_pos