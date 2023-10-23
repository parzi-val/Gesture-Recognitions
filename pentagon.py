import cv2
import mediapipe as mp
from utils import calculate_pentagon_area

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

image = cv2.imread("ClassesTutorials/cat.jpg")
image_height, image_width, _ = image.shape
# Initialize the webcam
cap = cv2.VideoCapture(0)
centrey = centrex = 0

pentagonArea = 0

framecount = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        centre = None
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

            if framecount % 40 == 0:
                tempPentagonArea = calculate_pentagon_area(top_node_coordinates) 
                if pentagonArea > tempPentagonArea:
                    print(f"{pentagonArea}>{tempPentagonArea} -->{(tempPentagonArea/pentagonArea)*100}% smaller")
                else:
                    print(f"{pentagonArea}<{tempPentagonArea} -->{(pentagonArea/tempPentagonArea)*100}% greater")
                pentagonArea = tempPentagonArea
            
                

            framecount += 1
    cv2.imshow('Hand Landmarks', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("done")
        break
    
cap.release()
cv2.destroyAllWindows()
