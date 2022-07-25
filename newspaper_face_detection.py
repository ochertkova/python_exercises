import zipfile
import PIL
from PIL import Image, ImageEnhance
import pytesseract
from pytesseract import Output
import cv2 as cv
import numpy as np

# loading the face detection classifier
#face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
zimages = zipfile.ZipFile('images.zip', 'r')
ilist = zimages.infolist()
img_list = []
img_text = ''

#function extracts text from img and converts it to a string
def extract_text (img):
    text_str = ''
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    #print(d.keys())
    im_size = img.size
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(float(d['conf'][i])) > 50:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv.rectangle(np.asarray(img), (x, y), (x + w, y + h), (0, 255, 0), 2)
    text_str = ' '.join([str(elem) for elem in d['text']])
    #imS = cv.resize(img, (int(im_size[0]/6), int(im_size[1]/6)))
    #cv.imshow('img', imS)
    #cv.waitKey(0)
    #print (text_str)
    return text_str

#function searches for a word match in image text
def search_word (word, i_text):
    if word in i_text:
        return True
    else:
        return False
    
#function searches for faces and creates a contact sheet
def find_face (img):
    im_size = img.size
    size_factor = 4
    imC = incr_contr(img)
    imS = cv.resize(np.asarray(imC), (int(im_size[0]/size_factor), int(im_size[1]/size_factor)))
    max_size = (100,100)
    print("[INFO] performing face detection...")
    
    #gray = cv.cvtColor(imS, cv.COLOR_BGR2GRAY)
    imS_gray = cv.cvtColor(imS, cv.COLOR_BGR2GRAY)
    face_coords = face_cascade.detectMultiScale(imS_gray, scaleFactor=1.05, minNeighbors=15, minSize=(15, 15), flags=cv.CASCADE_SCALE_IMAGE)
    print("[INFO] {} faces detected...".format(len(face_coords)))
    faces = [] #a list for cropped faces
    for (x, y, w, h) in face_coords:
        cv.rectangle(imS, (x, y), (x + w, y + h), (0, 255, 0), 2)
        im_crop = img.copy()
        #print ("x: {} y: {} xw: {} yh: {}".format(x, y, x + w,y + h))
        face_res = im_crop.crop((x*size_factor, y*size_factor, (x + w)*size_factor, (y + h)*size_factor))
        face_res.thumbnail(max_size)
        faces.append(face_res)
    #cv_show_image(imS)
    # create a contact sheet
    try:
        first_face=faces[0]
        sh_x=0
        sh_y=0
        (mw,mh) = calculate_cs(faces)
        #create contact sheet
        contact_sheet=PIL.Image.new(first_face.mode, (mw,mh))

        for face in faces:
     
        # paste the current image into the contact sheet
            contact_sheet.paste(face, (sh_x, sh_y) )
            if sh_x+face.width == contact_sheet.width:
                sh_x=0
                sh_y=sh_y+face.height
            else:
                sh_x=sh_x+face.width
        #contact_sheet = contact_sheet.resize((int(contact_sheet.width),int(contact_sheet.height) ))
        #display(contact_sheet)
        contact_sheet.show()

    except:
        print ("But there were no faces in that file!")
  

def cv_show_image(imS):
    cv.imshow('img', imS)
    cv.waitKey(0)

def incr_contr(imC):
    print ("[INFO] Increasing contrast...")
    # Sharpen 
    enhancer = ImageEnhance.Sharpness(imC)
    res = enhancer.enhance(2.0) 

    # Improve contrast
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(2.5)
    res.show()
    return res

def calculate_cs(faces):
    mw = 100
    mh = 100
    if len(faces) == 5:
        rows = 1
    else:
        rows = len(faces)//5 +1
    print(rows)
    print ("[INFO] Calculatng contact sheet size")
    mw = mw*5
    mh = mh*rows
    return (mw,mh)

word = input('Enter search word:')

# Main: open and iterate through zip file, extract text and perform search of the given word, recognize faces and create a contact sheet for each file

for f in ilist:
    f_name = f.filename
    print (f.filename)
    ifile = zimages.open(f)
    img = Image.open(ifile)
    #img.show()
    #display(img)
    img_text = extract_text(img)
    found = search_word(word,img_text)
    if found == True:
        print ("Results found in file {}".format(f.filename))
        #print(found)
        try:
            ff = find_face(img)           
        except:
            print ("No faces found")
    else:
        print ("No results found in file {}".format(f.filename))


#print(img_list)


    



#print (img_list[0])
#img_text = extract_text(img_list[0])
#print (img_text)
#word = input('Enter search word:')
#found = search_word(word,img_text)
#print(found)
#find_face (img_list[0])
