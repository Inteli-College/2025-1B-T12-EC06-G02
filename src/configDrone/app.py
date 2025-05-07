from djitellopy import Tello
import time

# Cria a instância do drone
tello = Tello()

# Conecta ao drone
tello.connect()
print(f"Nível da bateria: {tello.get_battery()}%")

# Decola
tello.takeoff()
time.sleep(3)

# Pousa
tello.land()