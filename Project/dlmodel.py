import os
import numpy as np
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity


def CalculateSimilarity(user_image_path):
    # Folder containing other images
    images_folder_path = 'image'

    # Load pre-trained MobileNetV2 model for feature extraction
    base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

    # Function to preprocess an image
    def preprocess_image(img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(np.expand_dims(img_array, axis=0))
        return img_array

    # Load features for the user image
    user_image_features = base_model.predict(preprocess_image(user_image_path))
    user_image_features = np.reshape(user_image_features, (1, -1))

    # List all image files in the folder
    img_files = [f for f in os.listdir(images_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', 'webp'))]

    # Calculate and store cosine similarity for each image
    similarities = []
    for img_file in img_files:
        img_path = os.path.join(images_folder_path, img_file)
        image_features = base_model.predict(preprocess_image(img_path))
        image_features = np.reshape(image_features, (1, -1))
        similarity = cosine_similarity(user_image_features, image_features)[0][0]
        similarities.append((img_file, similarity))

    # Sort the results by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    if similarities and similarities[0][1] >= 0.80:
        # Return the most similar image file and its similarity value
        most_similar_image, similarity_value = similarities[0]
        return most_similar_image, similarity_value
    else:
        # Return None if no similarity meets the threshold
        return None, None
#
# # Example usage:
# user_image_path = 'image/BGH_6_Quick Chef.webp'
# most_similar_image, similarity_value = CalculateSimilarity(user_image_path)
#
# if most_similar_image is not None:
#     print(f"user_image_path: {user_image_path}")
#     print(f"Most similar image: {most_similar_image}")
#     print(f"Similarity value: {similarity_value}")
# else:
#     print("No similar image found.")
