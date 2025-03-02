import cv2
from utils import stackIt, GetFPS


fps = GetFPS()
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_SETTINGS, 1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while cap.isOpened():
    _, img = cap.read()

    fps.draw_in_img(img)

    cv2.imshow("Automatic Attendence System", stackIt([[img]]))

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
