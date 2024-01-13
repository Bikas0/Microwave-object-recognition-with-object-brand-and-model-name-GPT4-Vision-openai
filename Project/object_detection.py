import os
import cv2
from transformers import DetrForObjectDetection
import torch
import supervision as sv
import torchvision
import warnings


def object(img_path):

    # Suppress TensorFlow warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    # Loading model
    model = DetrForObjectDetection.from_pretrained("custom-model")

    ANNOTATION_FILE_NAME = "annotations.json"
    DETECT_DIRECTORY = "detect"

    # Instantiate the image processor
    from transformers import DetrImageProcessor
    image_processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")

    class CocoDetection(torchvision.datasets.CocoDetection):
        def __init__(self, image_directory_path: str, image_processor, train: bool = True):
            super().__init__(image_directory_path, os.path.join(image_directory_path, ANNOTATION_FILE_NAME))
            self.image_processor = image_processor

        def __getitem__(self, idx):
            images, annotations = super().__getitem__(idx)
            image_id = self.ids[idx]
            annotations = {'image_id': image_id, 'annotations': annotations}
            encoding = self.image_processor(images=images, annotations=annotations, return_tensors="pt")
            pixel_values = encoding["pixel_values"].squeeze()
            target = encoding["labels"][0]

            return pixel_values, target

    # Use the image processor
    try:
        DETECT_DATASET = CocoDetection(image_directory_path=DETECT_DIRECTORY, image_processor=image_processor, train=True)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Utils
    categories = DETECT_DATASET.coco.cats
    id2label = {k: v['name'] for k, v in categories.items()}
    box_annotator = sv.BoxAnnotator()

    # User input for image path
    user_input_image_path = img_path
    # Load image
    image = cv2.imread(user_input_image_path)

    # Annotate detections
    with torch.no_grad():
        inputs = image_processor(images=image, return_tensors='pt')
        outputs = model(**inputs)

        target_sizes = torch.tensor([image.shape[:2]])
        results = image_processor.post_process_object_detection(outputs=outputs, threshold=0.10, target_sizes=target_sizes)[0]

        detections = sv.Detections.from_transformers(transformers_results=results)
        labels = [f"{id2label[class_id]} {confidence:.2f}" for _, confidence, class_id, _ in detections]

    label = labels[0].split(" ")[0]
    list_file = os.listdir('image')
    for file in list_file:
        root = file.split(".")[0]
        if root == label:
            return file

