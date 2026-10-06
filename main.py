import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
import time

cap = cv2.VideoCapture(0)

options = vision.HandLandmarkerOptions(
    base_options = mp.tasks.BaseOptions(model_asset_path="hand_landmarker.task"),
    num_hands = 1,
    running_mode = vision.RunningMode.VIDEO 
)

detector = vision.HandLandmarker.create_from_options(options)

h, w = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
mask = np.zeros((h,w), dtype=np.uint8)
board = np.full((h, w, 3), 255, dtype=np.uint8)
b_board = np.full((h, w, 3), (0, 0,0), dtype=np.uint8)

mode = "cam"

prev_point = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
    timestamp_ms = int(time.time()*1000)
    result = detector.detect_for_video(mp_image, timestamp_ms)

    if mode == "cam":
        layer = frame
    elif mode == "color":
        layer = b_board 
    
    sonuc = np.where(mask[..., None] == 255, layer, board)
    
    if result.hand_landmarks:
        lm = result.hand_landmarks[0]
        index_finger = lm[8]
        cx, cy = int(index_finger.x*w), int(index_finger.y*h)


        ids = [(8,6),(12,10),(16,14),(20,18)]
        boolean = [lm[tip].y < lm[pip].y for (tip, pip) in ids]
        print(boolean)

        control = (boolean == [True, False, False, False])

        if control:
            if prev_point is not None:
                cv2.line(mask, prev_point, (cx, cy), 255, 20)
            
            prev_point = (cx, cy)
            cv2.circle(mask, (cx, cy), 10, 255, cv2.FILLED)
        else:
            prev_point = None

        
        cv2.circle(sonuc, (cx, cy), 7, (0,0,255), cv2.FILLED)

    else:
        prev_point = None
    
    cv2.imshow("EraseVision", sonuc)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
    elif key == ord("c"):
        mask[:] = 0
        prev_point = None
    elif key == ord("m"):
        if mode == "cam":
            mode = "color"
        else:
            mode = "cam"

detector.close()
cap.release()
cv2.destroyAllWindows()
