import cv2
import os

# Specify the input and output directories
input_directory = "image"
output_directory = "resized_images"

# Check if the directory already exists
if not os.path.exists(output_directory):
    # If not, create the directory
    os.makedirs(output_directory)

# Get the list of files in the input directory
file_list = os.listdir(input_directory)

# Loop through each file in the input directory
for file_name in file_list:
    # Construct the full path to the input image
    input_image_path = os.path.join(input_directory, file_name)

    # Read the image using OpenCV
    image = cv2.imread(input_image_path)

    # Check if the image is successfully loaded
    if image is not None:
        # Specify the new dimensions (width, height)
        new_width = 512
        new_height = 512

        # Resize the image
        resized_image = cv2.resize(image, (new_width, new_height))

        # Construct the full path to the output image
        output_image_path = os.path.join(output_directory, file_name)

        # Save the resized image
        cv2.imwrite(output_image_path, resized_image)

        print(f"Resized and saved: {output_image_path}")
    else:
        print(f"Error: Unable to read the image at {input_image_path}")
