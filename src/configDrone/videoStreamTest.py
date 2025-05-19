from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

tello.streamon()
frame_read = tello.get_frame_read()

try:
    while True:
        frame = frame_read.frame

        # convert BGR to RGB
        frame_rgb = frame[..., ::-1]

        cv2.imshow("Tello stream", frame_rgb)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
finally:
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()
