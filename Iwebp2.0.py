import cv2
import numpy as np
import json
import argparse
from pyvirtualcam import Camera
import tkinter as tk
from tkinter import ttk

def load_config(config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}
    return config

def save_config(config, config_file):
    with open(config_file, "w") as f:
        json.dump(config, f)

def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        print("Impossibile leggere il frame dalla webcam IP.")
        return None
    return frame

def main(args):
    config_file = args.config_file
    default_ip = args.default_ip
    default_port = args.default_port

    config = load_config(config_file)
    ip_address = config.get("ip_address", default_ip)
    port = config.get("port", default_port)

    def save_config_and_start():
        ip_address = entry_ip_address.get()
        port = entry_port.get()
        frame_width = int(entry_frame_width.get())
        frame_height = int(entry_frame_height.get())
        fps = int(entry_fps.get())

        config = {"ip_address": ip_address, "port": port}
        save_config(config, config_file)

        ip_webcam_url = f"http://{ip_address}:{port}/video"
        cap = cv2.VideoCapture(ip_webcam_url)

        with Camera(width=frame_width, height=frame_height, fps=fps) as cam:
            print(f'Webcam virtuale avviata ({frame_width}x{frame_height} @ {fps} fps)')

            while True:
                frame = capture_frame(cap)
                if frame is None:
                    break

                resized_frame = cv2.resize(frame, (frame_width, frame_height))
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

                cam.send(rgb_frame)
                cam.sleep_until_next_frame()

    root = tk.Tk()
    root.title("Webcam IP to Virtual Webcam")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky="w")

    ttk.Label(frame, text="Indirizzo IP:").grid(row=0, column=0, padx=(0, 10))
    entry_ip_address = ttk.Entry(frame, width=15, textvariable=tk.StringVar(root, value=ip_address))
    entry_ip_address.grid(row=0, column=1)

    ttk.Label(frame, text="Porta:").grid(row=1, column=0, padx=(0, 10))
    entry_port = ttk.Entry(frame, width=5, textvariable=tk.StringVar(root, value=port))
    entry_port.grid(row=1, column=1)

    ttk.Label(frame, text="Larghezza frame:").grid(row=2, column=0, padx=(0, 10))
    entry_frame_width = ttk.Entry(frame, width=5, textvariable=tk.StringVar(root, value=args.frame_width))
    entry_frame_width.grid(row=2, column=1)

    ttk.Label(frame, text="Altezza frame:").grid(row=3, column=0, padx=(0, 10))
    entry_frame_height = ttk.Entry(frame, width=5, textvariable=tk.StringVar(root, value=args.frame_height))
    entry_frame_height.grid(row=3, column=1)

    ttk.Label(frame, text="Frequenza frame:").grid(row=4, column=0, padx=(0, 10))
    entry_fps = ttk.Entry(frame, width=5, textvariable=tk.StringVar(root, value=args.fps))
    entry_fps.grid(row=4, column=1)

    ttk.Button(frame, text="Avvia", command=save_config_and_start).grid(row=5, column=0, columnspan=2, pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acquisisci e inviati immagini da una webcam IP a una webcam virtuale.")
    parser.add_argument("--config_file", default="config.json", help="File di configurazione per memorizzare l'indirizzo IP e la porta della webcam IP.")
    parser.add_argument("--default_ip", default="192.168.1.00", help="Indirizzo IP predefinito.")
    parser.add_argument("--default_port", default="0000", help="Porta predefinita.")
    parser.add_argument("--frame_width", type=int, default=1280, help="Larghezza del frame.")
    parser.add_argument("--frame_height", type=int, default=720, help="Altezza del frame.")
    parser.add_argument("--fps", type=int, default=60, help="Frequenza dei frame.")

    args = parser.parse_args()
    main(args)