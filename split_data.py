# Taken from https://medium.com/mlearning-ai/training-yolov5-custom-dataset-with-ease-e4f6272148ad
# Training YOLOv5 custom dataset with ease
# by Luiz Doleron
import os, shutil, random

# preparing the folder structure

full_data_path = 'D:\ip_y8\data\obj\\'
extension_allowed = '.jpg'
split_percentage = 90

training_path = 'D:\ip_y8\data\\train'
if os.path.exists(training_path):
    shutil.rmtree(training_path)
os.mkdir(training_path)
    
validation_path = 'D:\ip_y8\data\\val'
if os.path.exists(validation_path):
    shutil.rmtree(validation_path)
os.mkdir(validation_path)
    
training_training_path = training_path + '\\images'
training_validation_path = training_path + '\\labels'
validation_training_path = validation_path + '\\images'
validation_validation_path = validation_path +'\\labels'
    
os.mkdir(training_training_path)
os.mkdir(validation_training_path)
os.mkdir(training_validation_path)
os.mkdir(validation_validation_path)

files = []

ext_len = len(extension_allowed)

for r, d, f in os.walk(full_data_path):
    for file in f:
        if file.endswith(extension_allowed):
            strip = file[0:len(file) - ext_len]      
            files.append(strip)

random.shuffle(files)

size = len(files)                   

split = int(split_percentage * size / 100)

print("Copying Training Data to train folder...")
for i in range(split):
    strip = files[i]
                         
    image_file = strip + extension_allowed
    src_image = full_data_path + image_file
    shutil.copy(src_image, training_training_path) 
                         
    annotation_file = strip + '.txt'
    src_label = full_data_path + annotation_file
    shutil.copy(src_label, training_validation_path) 

print("Copying Validation Data to val folder...")
for i in range(split, size):
    strip = files[i]
                         
    image_file = strip + extension_allowed
    src_image = full_data_path + image_file
    shutil.copy(src_image, validation_training_path) 
                         
    annotation_file = strip + '.txt'
    src_label = full_data_path + annotation_file
    shutil.copy(src_label, validation_validation_path) 

print("Data Copy Finished.")