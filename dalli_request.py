# imports
from openai import OpenAI  # OpenAI Python library to make API calls
import requests  # used to download images
import os  # used to access filepaths
from PIL import Image  # used to print and edit images

# initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

# set a directory to save DALL·E images to
image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}")


# create an image

# set the prompt, max len is 1,000 char for dal2, 4000 for dal3
prompt="A living room, in a california spanish style bungalo, is 20 feet wide and 40 feet long and 8 feet tall. The floors are 2 inch wide golden oak boards. There is a simple fireplace that protrudes from the wall slightly, on one of the longer walls. the firplace includes a mantle with an indent in california spanish style.  There is a window on one of the shorter walls.  The other shorter wall has a large open doorway to the dining room"
#prompt = "A cyberpunk monkey hacker dreaming of a beautiful bunch of bananas, digital art"
#prompt = "a mechanicanl design to open a  garbage can lid when the drawer holding the garbage can is opened"
#prompt = "A front yard garden of a California Spanish Style home, with native plants including golden poppies,sages, Arctostaphylos, California fuchsia, California Rose, Ceanothus, Penstemon, Bush Monkeyflower, and California lilac. The garden contains a garden gnome on the ground next to a plant.   There should be a curved brick path that runs from the front door to the sidewalk.  The garden is sloped towards the street at a 30 degree angle. The image should be from the view of a person standing 10 feet in front of the garden and on a 10 foot ladder" 
#prompt = "A front yard garden, that is 40 feet wide and 30 feet deep, of a California Spanish Style home, with native plants  including golden poppies,sages, Arctostaphylos, California fuchsia, California Rose, Ceanothus, Penstemon, Bush Monkeyflower, and California lilac. There should be a curved path that runs from the front door to the sidewalk.  The garden is sloped towards the street at a 30 degree angle. The image should be from the view of a person standing 10 feet in front of the garden and on a 10 foot ladder" 

# call the OpenAI API
generation_response = client.images.generate(
    model = "dall-e-3",
    prompt=prompt,
    n=1,
    quality="hd",
    size="1024x1024",
    response_format="url",
    style="natural",
)

# print response
print(generation_response)

# save the image
generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)
generated_image_url = generation_response.data[0].url  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file


# print the image
#display(Image.open(generated_image_filepath))

# image locations
print('\n\n\n')
print('Image filepath:', generated_image_filepath)
print('Image URL:',generated_image_url)
