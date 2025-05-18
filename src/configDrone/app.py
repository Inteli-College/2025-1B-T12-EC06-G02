from djitellopy import Tello
import time

def test_basic_movement():
    print("=== TESTE DE MOVIMENTO DO TELLO ===")
    tello = Tello()

    try:
        tello.connect()
        battery = tello.get_battery()
        print(f"Bateria: {battery}%")
        if battery < 20:
            print("⚠️ Bateria baixa! Carregue antes de continuar.")
            return False

        print("Decolando...")
        tello.takeoff()
        time.sleep(5)

        movimentos = [
            ("Subir 50cm", lambda: tello.move_up(50)),
            ("Frente 50cm", lambda: tello.move_forward(20)),
            ("Direita 50cm", lambda: tello.move_right(20)),
            ("Esquerda 50cm", lambda: tello.move_left(20)),
            ("Trás 50cm", lambda: tello.move_back(20)),
            ("Descer 30cm", lambda: tello.move_down(30)),
            ("Girar horário 90°", lambda: tello.rotate_clockwise(90)),
            ("Girar anti-horário 90°", lambda: tello.rotate_counter_clockwise(90)),
        ]

        for nome, func in movimentos:
            print(f"\nExecutando: {nome}")
            func()
            time.sleep(3)

        print("Pousando...")
        tello.land()
        return True

    except Exception as e:
        print(f"❌ Erro: {e}")
        try:
            tello.land()
        except:
            pass
        return False

if __name__ == "__main__":
    test_basic_movement()
