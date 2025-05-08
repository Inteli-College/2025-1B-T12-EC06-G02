import cv2
from djitellopy import Tello
import time

# Initialize Tello
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")
tello.streamon()
frame_read = tello.get_frame_read()

# State
flying = False
photo_counter = 0
SPEED = 200  # movement speed

# Velocity state
lr = 0  # left/right
fb = 0  # forward/backward
ud = 0  # up/down
yaw = 0  # rotation

print("""
Connected to Tello!
Controls:
  W/A/S/D: Forward/Left/Backward/Right
  Q/E    : Rotate left/right
  8/5 : Up / Down
  P      : Take photo
  L      : Takeoff / Land
  0      : Exit and disconnect
""")

try:
    while True:
        key = cv2.waitKey(1) & 0xFF
        # Reset velocity
        lr = fb = ud = yaw = 0

        # Handle basic movement
        if key == ord('w'):
            fb = SPEED
        elif key == ord('s'):
            fb = -SPEED
        elif key == ord('a'):
            lr = -SPEED
        elif key == ord('d'):
            lr = SPEED
        elif key == ord('q'):
            yaw = -SPEED
        elif key == ord('e'):
            yaw = SPEED
        elif key == ord('8'):
            ud = SPEED
        elif key == ord('5'):
            ud = -SPEED
        elif key == ord('p'):
            filename = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, frame_read.frame)
            print(f"Photo taken: {filename}")
        elif key == ord('l'):
            if not flying:
                tello.takeoff()
                flying = True
                print("Takeoff")
            else:
                tello.land()
                flying = False
                print("Landing")
        elif key == ord('0'):
            print("Disconnecting...")
            break

        # Send current velocities to drone
        tello.send_rc_control(lr, fb, ud, yaw)

        # Apply blue tint fix (convert BGR to RGB)
        frame = frame_read.frame
        frame_rgb = frame[..., ::-1]

        # Show corrected frame
        cv2.imshow("Tello Stream (Corrected)", frame_rgb)

except KeyboardInterrupt:
    print(" Interrupted by user")

finally:
    tello.send_rc_control(0, 0, 0, 0)
    tello.streamoff()
    tello.end()
    cv2.destroyAllWindows()
    print(" Disconnected cleanly")
