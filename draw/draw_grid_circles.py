from PIL import Image, ImageDraw
import random

# Dimensions of the image
image_width = 1000
image_height = 1000

# Create a blank image with a white background
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)


def main():
    # Define the number of circles and the radius increment
    num_circles = 10

    # Calculate the number of boxes in each row and column of the grid
    num_boxes = image_width

    # Calculate the center point of the image
    center_x = image_width // 2 - 100
    center_y = image_height // 2 - 200
    # place the center in the middle of a unit box
    center_x += 0.5
    center_y += 0.5

    circle_radii = [random.choice(range(40, 1000)) for _ in range(num_circles)]
    scale_factor = 10
    annuli_thickness = 9
    for x in range(num_boxes):
        for y in range(num_boxes):
            # Calculate the coordinates of the bounding box
            left = x * scale_factor
            top = y * scale_factor
            right = left + scale_factor
            bottom = top + scale_factor
            # for each box iterate through the circles and see if it is intersected by any of them
            for i, circle_radius in enumerate(circle_radii):
                distance = ((left - center_x)**2 + (bottom - center_y)**2) ** 0.5
                if circle_radius - (annuli_thickness) <= distance <= circle_radius:
                    # Start white and get increasingly darker shades of grey as move toward outer circles
                    gray_value = int((1 / ((distance + 200) / (image_width // 2))) * (200))
                    color = (gray_value, gray_value, gray_value)
                    break
                else:
                    # Set the background color as a random light gray
                    background_gray_value = random.randint(200, 255)
                    color = (background_gray_value, background_gray_value, background_gray_value)

            # Draw the box with the calculated color
            draw.rectangle([left, top, right, bottom], fill=color)

    # Save the image as a PNG file
    image.save("circles_on_grid.png")
    print("Image saved as 'circles_on_grid.png'.")

if __name__ == '__main__':
    main()
