import time

def countdown(sec : int):
    while sec > 0:
        print(f"Retrying in {sec} seconds")
        time.sleep(1)
        sec -= 1