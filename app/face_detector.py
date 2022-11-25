import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from scipy.spatial import distance


def cos_sim(A, B):
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))


def make_base_image(check, image):
    app = FaceAnalysis(providers=['CPUExecutionProvider']) #'CUDAExecutionProvider',
    app.prepare(ctx_id=0, det_size=(640, 640))

    #embeddings_list = ''
    image = cv2.resize(image , (640,640))
    image =  cv2.flip(image, 1)

    faces = app.get(image , max_num=1)
    if len(faces) == 0:
        return check, None
    # rimg = app.draw_on(image, faces)

    face_landmark_list = faces[0]['landmark_2d_106']
    eye_euclidean = distance.euclidean(face_landmark_list[38] , face_landmark_list[88])
    
    if face_landmark_list[72][0] + 9 <= face_landmark_list[86][0] and eye_euclidean < 80: 
        embeddings_list = faces[0]['embedding']
        result = 'right'
    elif face_landmark_list[72][0] >= face_landmark_list[86][0] + 9 and eye_euclidean < 80:
        embeddings_list = faces[0]['embedding']
        result = 'left'
    else:
        embeddings_list = faces[0]['embedding']
        result = 'front'
    
    if check == result:
        return result, embeddings_list
    else:
        return result, None

def check_image(img, embedding):    
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    faces = app.get(img , max_num=3)
    result = "0"
    print(len(faces))
    if len(faces) > 1:
        for face in faces:
            target = face['embedding']
            for i in embedding:
                euclideans = cos_sim(target , i)
                if euclideans >= 0.4:
                    result = "1"
                    break
    elif len(faces) == 1:
        target = faces[0]['embedding']
        for i in embedding:
            euclideans = cos_sim(target , i)
            if euclideans >= 0.4:
                result = "1"
                break
    return result
