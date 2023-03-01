from Constants import AI_MODEL_PATH
import tensorflow as tf
import mediapipe as mp
import numpy as np
import cv2

def detect() -> str:
    """
    Method, which detects the sign language and returns the result as a string.
    @Params:
        None
    @Returns:
        result: str - The result of the detection in english.
    """

    model = tf.keras.models.load_model(AI_MODEL_PATH)

    mp_holistic = mp.solutions.holistic # Holistic model
    mp_drawing = mp.solutions.drawing_utils # Drawing utilities

    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5

    actions = np.array(['hello', 'thanks', 'iloveyou'])
    
    cap = cv2.VideoCapture(1)
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():

            # Read feed
            _, frame = cap.read()

            # Make detections
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw landmarks
            # Draw face connections
            mp_drawing.draw_landmarks(
                image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
            ) 

            # Draw pose connections
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
            ) 

            # Draw left hand connections
            mp_drawing.draw_landmarks(
                image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
            ) 
            # Draw right hand connections  
            mp_drawing.draw_landmarks(
                image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            ) 
            
            # 2. Prediction logic
            pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
            face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
            lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
            rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
            keypoints = np.concatenate([pose, face, lh, rh])
            sequence.append(keypoints)
            sequence = sequence[-30:]
            
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                predictions.append(np.argmax(res))
                
            #3. Viz logic
                if np.unique(predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > threshold: 
                        
                        if len(sentence) > 0: 
                            if actions[np.argmax(res)] != sentence[-1]:
                                sentence.append(actions[np.argmax(res)])
                        else:
                            sentence.append(actions[np.argmax(res)])

                if len(sentence) > 5: 
                    sentence = sentence[-5:]

            # Show to screen
            cv2.imshow('OpenCV Feed', image)

            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    return " ".join(sentence)

if __name__ == "__main__" :
    detect()