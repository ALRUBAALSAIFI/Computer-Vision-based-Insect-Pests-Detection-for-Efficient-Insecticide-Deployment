import cv2
import argparse
import os
from ultralytics import YOLO
import supervision as sv
import numpy as np
import pyodbc
from datetime import date
from datetime import datetime

insectClasses = ['beetle', 'earwig','grasshopper','moth','wasp','weevil','ants','caterpillar','aphids','bee','butterfly','fly','dragonfly','spider']
strCamerID = "USBCam1"

connectionString = ("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-197CJBT;"
            "Database=IPDMS;"
            "UID=sa;"
            "PWD=abcd1234!;"
            "Trusted_Connection=yes;")
dbsvrConnection = pyodbc.connect(connectionString)
dbsvrCursor = dbsvrConnection.cursor()

ZONE_POLYGON = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1]
])

confidenceRate = 0.9

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def main():
    frameNo = 0
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution
        
    # Uncomment to use a webcam attached to the PC/Laptop
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    model = YOLO("D:\\ip_train_y8\\YOLOv8Model.pt")
    
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True,verbose = False)[0]
        detections = sv.Detections.from_yolov8(result)
        # detections = detections[detections.class_id == 7]
        detections = detections[detections.confidence >= confidenceRate]
                
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _,_, confidence, class_id, _
            in detections
        ]
    
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )
        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)    
        
        if(len(detections) > 0):
            sqlINSERTQuery = ''
            frameNo += 1
            for detection in detections:
                strFileName = "Class " + insectClasses[detection[3]] + ", Frame " + str(frameNo) + ", Confidence " + "{:.2f}".format(detection[2]) + ".jpg"
                strFolderName = "D:\ip_train_y8\detections"
                cv2.imwrite(os.path.sep.join([strFolderName, strFileName]),frame)
                # print(strFileName)
                # print("Confidence: " + "{:.2f}".format(detection[2]))
                # print("Class: " + insectClasses[detection[3]])
                picFileName = os.path.sep.join([strFolderName, strFileName])
                binFile = convertToBinaryData(picFileName)
                sqlINSERTQuery = "INSERT INTO tbl_DETECTIONS(DetectionCode,DetectionDate,DetectionTime,"
                sqlINSERTQuery = sqlINSERTQuery + "InsectClass,CameraID,DetectionImage,NumberOfDetections,"
                sqlINSERTQuery = sqlINSERTQuery + "ConfidenceRating) VALUES(?,?,?,?,?,?,?,?)"
                sqlINSERTQueryValues = (insectClasses[detection[3]] + "-" + str(frameNo),date.today(),datetime.now().strftime("%I:%M:%S %p"),insectClasses[detection[3]],"CamUSB1",binFile,len(detections),float("{:.2f}".format(detection[2])))
                dbsvrCursor.execute(sqlINSERTQuery,sqlINSERTQueryValues)
                dbsvrConnection.commit()
            
        cv2.imshow("Insect Pest Detection using YOLOv8 [Press Esc to Exit]", frame)

        if (cv2.waitKey(1) == 27):
            cv2.destroyAllWindows()
            dbsvrCursor.close()
            dbsvrConnection.close()
            break

if __name__ == "__main__":
    main()