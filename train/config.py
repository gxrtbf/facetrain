import dlib

DETECTOR_PATH = ""
ALIGN_PATH = "train/model/shape_predictor_68_face_landmarks.dat"
NET_VECTOR_PATH = "train/model/dlib_face_recognition_resnet_model_v1.dat"

detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(ALIGN_PATH)
face_net_model = dlib.face_recognition_model_v1(NET_VECTOR_PATH)