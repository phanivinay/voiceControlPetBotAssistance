import cv2
import mediapipe as mp
import random
import time
import pyttsx3

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Define gestures
gesture_dict = {
    (0, 0, 0, 0, 0): "rock",       # Fist (rock)
    (1, 1, 1, 1, 1): "paper",      # All fingers open (paper)
    (0, 1, 1, 0, 0): "scissors"    # Two fingers open (scissors)
}

def get_hand_gesture(landmarks):
    """ Convert finger positions to a gesture. """
    finger_up = []
    
    # Thumb
    finger_up.append(1 if landmarks[4].x < landmarks[3].x else 0)
    
    # Other four fingers
    for i in [8, 12, 16, 20]:
        finger_up.append(1 if landmarks[i].y < landmarks[i - 2].y else 0)

    return gesture_dict.get(tuple(finger_up), "unknown")

def speak(text):
    """ Use TTS to announce the computer's move. """
    engine.say(text)
    engine.runAndWait()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame for a mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert to RGB (MediaPipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame for hand landmarks
    result = hands.process(rgb_frame)
    
    player_move = "none"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Detect gesture
            player_move = get_hand_gesture(hand_landmarks.landmark)
            cv2.putText(frame, f"Your Move: {player_move}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Generate computer move with a countdown
    if player_move != "none":
        for i in range(3, 0, -1):
            cv2.putText(frame, f"Computer will play in: {i}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Rock Paper Scissors", frame)
            time.sleep(1)  # 1 second delay for countdown

        computer_move = random.choice(["rock", "paper", "scissors"])
        speak(computer_move)  # Announce computer's move
        cv2.putText(frame, f"Computer: {computer_move}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Determine Winner
        winner = "Waiting..."
        if player_move == computer_move:
            winner = "It's a tie!"
        elif (player_move == "rock" and computer_move == "scissors") or \
             (player_move == "paper" and computer_move == "rock") or \
             (player_move == "scissors" and computer_move == "paper"):
            winner = "You win!"
        else:
            winner = "Computer wins!"

        cv2.putText(frame, winner, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    # Show the frame
    cv2.imshow("Rock Paper Scissors", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
