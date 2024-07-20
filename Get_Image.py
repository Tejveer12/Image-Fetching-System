import cv2
from deepface import DeepFace
import os


# Function to get the cropped image using DeepFace for face detection
def get_cropped_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    default_image = cv2.imread("demo.jpg")
    default_image = cv2.resize(default_image, (512, 512))

    if image is None:
        print(f"Error: Unable to load image {image_path}")
        return default_image

    # Detect faces in the image using DeepFace
    detected_faces = DeepFace.extract_faces(image, detector_backend='yolov8')

    if len(detected_faces) == 0:
        print("No faces found in the image.")
        return default_image

    x = detected_faces[0]['facial_area']['x']
    y = detected_faces[0]['facial_area']['y']
    w = detected_faces[0]['facial_area']['w']
    h = detected_faces[0]['facial_area']['h']

    # Add margins to the face bounding box
    margin = 200
    x = max(0, x - margin)
    y = max(0, y - margin)
    w = min(image.shape[1], w + 2 * margin)
    h = min(image.shape[0], h + 2 * margin)

    # Crop the face region from the image
    cropped_image = image[y:y + h, x:x + w]
    resized_image = cv2.resize(cropped_image, (512, 512))

    return resized_image


# Function to get image IDs and their corresponding images
def get_image_by_id(messages, dataset_path):
    # Placeholder image path for non-existing directories
    default_image = cv2.imread("demo.jpg")
    default_image = cv2.resize(default_image, (512, 512))

    # Process each ID sequentially
    results = []
    for entity in messages:
        if entity.lower().startswith("error"):
            value = entity.split(":")[1].strip()
            results.append({"ERROR": value})
            continue

        if entity.lower().startswith("success"):
            value = entity.split(":")[1].strip()
            results.append({"SUCCESS": value})
            continue

        id_directory = os.path.join(dataset_path, entity)

        # Check if directory exists
        if not os.path.exists(id_directory):
            results.append({entity: default_image})  # Return demo.jpg as cv2 image
            continue

        # Collect image files in the directory
        image_files = sorted([os.path.join(id_directory, file) for file in os.listdir(id_directory)])

        # Check if there are any image files in the directory
        if not image_files:
            results.append({entity: default_image})
            continue

        # Find the most front-facing image
        image = get_cropped_image(image_files[0])

        # If image is None, use the placeholder image
        if image is None:
            results.append({entity: default_image})
        else:
            results.append({entity: image})

    return results


