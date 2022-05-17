from decimal import Inexact
import cv2
import mediapipe as mp

# define a video capture object
vid = cv2.VideoCapture(0)

mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils


while(True):
	# Capture the video frame
	# by frame
    ret, frame = vid.read()
    index_finger_x = 0

    RGB_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks
    
    if multiLandMarks:
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(frame, handLms, mp_Hands.HAND_CONNECTIONS)
        index_finger_x = multiLandMarks[0].landmark[8].x
        index_finger_y = multiLandMarks[0].landmark[8].y
        index_finger_5 = multiLandMarks[0].landmark[5].y


        font = cv2.FONT_HERSHEY_SIMPLEX

        
        # org
        org = (50, 50)
        org2 = (100,100)
        
        # fontScale
        fontScale = 1
        
        color = (255, 0, 0)
        
        thickness = 2
        frame = cv2.putText(frame, str(index_finger_x), org, font, 
                        fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, str(index_finger_y), org2, font, 
                        fontScale, color, thickness, cv2.LINE_AA)

        if index_finger_y > index_finger_5:
            print("down")
        
        else:
            print("up")

    cv2.imshow('frame', frame)
	
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()