import os
id_directory = "Dataset/2020CSAI016"
image_files = [os.path.join(id_directory, file) for file in os.listdir(id_directory)]
image_files = sorted(image_files)
print(image_files)