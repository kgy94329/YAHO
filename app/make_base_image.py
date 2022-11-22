import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
import time
import os
from numpy import arcsin
from numpy.linalg import norm
from numpy import dot
from scipy.spatial import distance

## S 누르면 입력 받도록.


def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))


def make_base_image(user_name):
    cap = cv2.VideoCapture(0)

    app = FaceAnalysis(providers=[ 'CPUExecutionProvider']) #'CUDAExecutionProvider',
    app.prepare(ctx_id=0, det_size=(640, 640))

    pos = ['front' , 'right' ,'left']
    embeddings_list = list()
    face_landmark_list = list()
    texts = ['Look at the camera & Press button "S" to save' , 'Turn your face to the right and press the s key.' , 'Turn your face to the left and press the s key']
    count = 0

    if user_name not in os.listdir():
        os.mkdir(f'./{user_name}')
    else:
        pass

    file_path = f'./{user_name}/'

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.resize(image , (640,640))
        image =  cv2.flip(image, 1)
        image = cv2.putText(image, texts[count], (50,50), cv2.FONT_ITALIC, 0.7, (255,0,0), 1)

        
        key = cv2.waitKey(5)
        if key & 0xFF == 115:
            faces = app.get(image , max_num=1)
            
            rimg = app.draw_on(image, faces)
            if count == 0:  
                cv2.imwrite(f"{file_path}{user_name}_{pos[count]}.jpg", rimg)
                face_landmark_list.append(faces[0]['landmark_2d_106'])
                embeddings_list.append(faces[0]['embedding'])
                image += 200
                count += 1

            elif count == 1:
                face_landmark_list.append(faces[0]['landmark_2d_106'])
                eye_euclidean = distance.euclidean(face_landmark_list[-1][38] , face_landmark_list[-1][88])
                if face_landmark_list[0][86][0] < face_landmark_list[-1][86][0] and eye_euclidean < 50: 
                    cv2.imwrite(f"{file_path}{user_name}_{pos[count]}.jpg", rimg)
                    embeddings_list.append(faces[0]['embedding'])
                    image += 200
                    count += 1
                    print('right')
                else:
                    print('얼굴을 똑바로 돌리십시오.')

            elif count == 2: 
                face_landmark_list.append(faces[0]['landmark_2d_106'])
                eye_euclidean = distance.euclidean(face_landmark_list[-1][38] , face_landmark_list[-1][88])
                if face_landmark_list[0][86][0] > face_landmark_list[-1][86][0] and eye_euclidean < 50:
                    cv2.imwrite(f"{file_path}{user_name}_{pos[count]}.jpg", rimg)
                    embeddings_list.append(faces[0]['embedding'])
                    image += 200
                    count += 1
                    print('left')
                else:
                    print('얼굴을 똑바로 돌리십시오.')

            if count == 3:
                break  

        cv2.imshow('MediaPipe Face Mesh',image) # cv2.flip(image, 1)

        if key & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    

    cv2.destroyAllWindows()
    cap.release()
    return embeddings_list


def check_image(img , user_id , embedding):    
    app = FaceAnalysis(providers=[ 'CPUExecutionProvider']) #'CUDAExecutionProvider',
    app.prepare(ctx_id=0, det_size=(640, 640))
    faces = app.get(img , max_num=1)
    embeddings = faces[0]['embedding']
    result = 0
    for i in embedding:
        euclideans = cos_sim(embeddings , i)
        if euclideans >= 0.4:
            result = 1
            break
    return result
            
        
    