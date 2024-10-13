from ultralytics import YOLO

model = YOLO()

model.train(data="D:\ip_train_y8\dataset.yaml", epochs = 20)