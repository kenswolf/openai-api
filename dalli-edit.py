from openai import OpenAI  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images
import random

from io import BytesIO

def change_pixel_values_from_bytes(png_bytes, mask):
    # Create an in-memory file-like object
    img_buffer = BytesIO(png_bytes)

    # Open the image from the in-memory buffer
    img = Image.open(img_buffer)

    # Get the image size
    width, height = img.size

    # Access pixel values and modify them (example: invert colors)
    for x in range(width):
        for y in range(height):

            current_mask_pixel = mask.getpixel((x,y))
            r,g,b,t = current_mask_pixel
            if t == 1:


                # Get the pixel value at the current position (x, y)
                current_pixel = img.getpixel((x, y))

                # Modify the pixel value (example: invert colors)
                new_pixel = tuple(255 - value for value in current_pixel)

                # Update the pixel value at the current position
                img.putpixel((x, y), new_pixel)

    # Save the modified image to a new in-memory buffer
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')

    # Get the bytes of the modified image
    modified_png_bytes = output_buffer.getvalue()

    return modified_png_bytes

##################################

# initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))


# set a directory to save DALL·E images to
image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)

# create a mask
width = 1024
height = 1024
mask = Image.new("RGBA", (width, height), (0, 0, 0, 1))  # create an opaque image mask

"""
# set the bottom half to be transparent
for x in range(width):
    for y in range(height // 2, height):  # only loop over the bottom half of the mask
        # set alpha (A) to zero to turn pixel transparent
        alpha = 0
        mask.putpixel((x, y), (0, 0, 0, alpha))
"""


# Pick random top-left corner coordinates
side_x = 200
side_y = 100
top_left_x = random.randint(0, 512 - side_x - 10) + 512
top_left_y = random.randint(0, 512 - side_y - 10) + 512

for x in range(top_left_x, top_left_x + side_x):
    for y in range(top_left_y, top_left_y + side_y):
        # set alpha (A) to zero to turn pixel transparent
        alpha = 0
        mask.putpixel((x, y), (0, 0, 0, alpha))

print(f"Duck is in the {side_x} by {side_y} square that has an upper left corner at ({top_left_x},{top_left_y})")

# save the mask
mask_name = "bottom_half_mask.png"
mask_filepath = os.path.join(image_dir, mask_name)
mask.save(mask_filepath)


#################################

# note prompt should describe entire image, not just the masked area

prompt = "A front yard garden of a California Spanish Style home, with native plants including golden poppies,sages, Arctostaphylos, California fuchsia, California Rose, Ceanothus, Penstemon, Bush Monkeyflower, and California lilac. The garden contains a garden gnome on the ground next to a plant.   There should be a curved brick path that runs from the front door to the sidewalk. In the garden, on the ground, is a mouse.  The garden is sloped towards the street at a 30 degree angle. The image should be from the view of a person standing 10 feet in front of the garden and on a 10 foot ladder"

#prompt = "A golden poppy flower is growing.  It has four petals and a green stem."
#prompt = "A bright pink garden squirrel eating a nut"
#prompt = "Add a tree to the front yard.  Replace bricks below stairs, with flagstone pavers.  Add more golden poppy flowers"
#After a heavy rain, water covers the sidewalk and the  lower few feet of the front garden"

#################################


# edit an image

# call the OpenAI API
edit_response = client.images.edit(
    image=open(generated_image_filepath, "rb"),  # from the generation section
    mask=open(mask_filepath, "rb"),  # from right above
    prompt=prompt,  # from the generation section
    n=1,
    size="1024x1024",
    response_format="url",
)

# print response
print(edit_response)


# save the image
edited_image_name = "edited_image.png"  # any name you like; the filetype should be .png
edited_image_filepath = os.path.join(image_dir, edited_image_name)
edited_image_url = edit_response.data[0].url  # extract image URL from response
edited_image = requests.get(edited_image_url).content  # download the image

with open(edited_image_filepath, "wb") as image_file:
    image_file.write(edited_image)  # write the image to the file

# DEBUG
windowed_image = change_pixel_values_from_bytes(edited_image, mask)
windowed_edited_image_name = "windowed_edited_image.png"  # any name you like; the filetype should be .png
edited_image_filepath = os.path.join(image_dir, windowed_edited_image_name)
with open(edited_image_filepath, "wb") as image_file:
    image_file.write(windowed_image)  # write the image to the file

print('old image filepath:', generated_image_filepath)
print('new image filepath:', edited_image_filepath)
