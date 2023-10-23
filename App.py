import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import PhotoImage
from threading import Thread, Event, Condition
from gui import ImageZoomApp
from utils import calculate_pentagon_area
from queue import Queue

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize the webcam
cap = cv2.VideoCapture(0)

pentagonArea = 0
framecount = 0

# Create an event to gracefully exit both threads
exit_event = Event()
message_queue = Queue()
message_condition = Condition()  # Create a condition variable

# Create a Tkinter GUI
root = tk.Tk()
app = ImageZoomApp(root)

def open_cv_thread():
    global pentagonArea
    global framecount

    while not exit_event.is_set():
        ret, frame = cap.read()

        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
            # Create a list to store the top nodes of each finger
                top_nodes = [4, 8, 12, 16,20]

                # Store the 2D screen coordinates of top nodes
                top_node_coordinates = []
                tnc = top_node_coordinates
                for i, landmark in enumerate(hand_landmarks.landmark):
                    height, width, _ = frame.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    if i == 0:
                        centre = (cx,cy)

                    # Determine the color based on whether it's a top node of a finger
                    if i in top_nodes:
                        color = (0, 255, 0)  # Green for top nodes
                        top_node_coordinates.append((cx, cy))
                        cv2.circle(frame, (cx, cy), 5, color, -1)

                for i in range(len(top_node_coordinates)):
                    cv2.line(frame,top_node_coordinates[i],top_node_coordinates[(i+1)%len(top_node_coordinates)],(255,0,0),2)

                # Calculate the area of the pentagon
                temp_pentagon_area = calculate_pentagon_area(top_node_coordinates)

                # Compare the areas and put the result in the display queue
                if framecount % 40 == 0:
                    if pentagonArea > temp_pentagon_area:
                        with message_condition:
                            message_queue.put("smaller")
                            message_condition.notify()
                        print(f"{pentagonArea} > {temp_pentagon_area} --> {(temp_pentagon_area / pentagonArea) * 100}% smaller")
                        
                    else:
                        with message_condition:
                            message_queue.put("greater")
                            message_condition.notify()
                        print(f"{pentagonArea} < {temp_pentagon_area} --> {(pentagonArea / temp_pentagon_area) * 100}% greater")
                    pentagonArea = temp_pentagon_area

                framecount += 1

        cv2.imshow('Hand Landmarks', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("done")
            break

    cap.release()
    cv2.destroyAllWindows()

# Create and start the OpenCV thread
opencv_thread = Thread(target=open_cv_thread)
opencv_thread.start()

def display_tkinter():
    while not exit_event.is_set():
        with message_condition:
            message_condition.wait()  # Wait for the notification
            message = message_queue.get()
            if message == "smaller":
                app.zoom_image(False)
            elif message == "greater":
                app.zoom_image(True)
            root.update()

# Create and start the Tkinter thread
tkinter_thread = Thread(target=display_tkinter)
tkinter_thread.start()

root.mainloop()

# Set the exit_event when you want to exit both threads (e.g., when you close the Tkinter window)
exit_event.set()
opencv_thread.join()
tkinter_thread.join()
