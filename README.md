# HackStar
First you should have pycharm and python 3.7 version
then you need to install 

pip install Django
pip install sounddevice
pip instal keyboard
pip intall PyAutoGUI
pip intall opencv-python3
pip install opencv-contrib-python
pip install numpy

once you have done with your installation then write the following commands

also you need to create folder for storing pics which were captured for the face dectection and recognition
and specify that path in the view.py file 

def home2(request):

    def active():
        face_classifier = cv2.CascadeClassifier(
            'C:/Users/pranalii/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

			# path where haarcascade_frontalface_default.xml is present 
			
        def face_extractor(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if faces is ():
                return None
            for (x, y, w, h) in faces:
                cropped_face = img[y:y + h, x:x + w]

            return cropped_face

        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_name_path = 'C:/Users/pranalii/PycharmProjects/photos/user' + str(count) + '.jpg'
				
				#path of the folder in which images will be stored and the name of the images will be like user1.jpg,user2.jpg....
                
				cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)
            else:
                print("Face not found")
                pass
            if cv2.waitKey(1) == 13 or count == 60:
                break
        cap.release()
        cv2.destroyAllWindows()
        print("Collecting Samples Complete")
    active()
    return render(request, 'home2.html')
	
	
	
data_path = 'C:/Users/pranalii/PycharmProjects/photos/'

	#path of the folder in which images will be stored and the name of the images will be like user1.jpg,user2.jpg....

onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
Training_Data, Labels = [], []
for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)
Labels = np.asarray(Labels, dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Training_Data), np.asarray(Labels))
print("Model trained successfully")
face_classifier = cv2.CascadeClassifier('C:/Users/pranalii/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

	# path where haarcascade_frontalface_default.xml is present 
			
def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi


cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    image, face = face_detector(frame)
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        results = model.predict(face)
        if results[1] < 500:
            confidence = int(100 * (1 - (results[1])/300))
            display_string = str(confidence) + '% Confident it is User'
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 120, 150), 2)
        if confidence > 75:
            cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Face Recognition', image)
        else:
            cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Recognition', image)
    except Exception:
        cv2.putText(image, "No Face Found", (220, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Face Recognition', image)
        pass
    if cv2.waitKey(1) == 13:
        break
cap.release()
cv2.destroyAllWindows()

	
you are done with all this then you need to make migrations by using 
	python manage.py makemigrations 
commands after this 
	python manage.py migrate 
command then finally 
	python manage.py runserver



