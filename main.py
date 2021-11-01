# For this application we'll be using python's cv2 module
import smtplib
import cv2
# We'll be using winsound module for audio operations
import winsound

# This function performs mail operation(i.e, sending mail at apropriate moment)
def sendMail():

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication note: This mail id will be used and if any security breach will be detected, the email from this ID will be sent to reciever's mail id
    s.login("pydemo9876@gmail.com", "qwertyuiopoiuytrewq")
    
    # message to be sent from Sender to Reciever
    message = "Security Breach Detected!!!"
    
    # sending the mail
    s.sendmail("pydemo9876@gmail.com", "omkar.nangare20@pccoepune.org", message)
    
    # terminating the session
    s.quit()



 #VideoCapture(index) gets a video capture object for the camera.
# Index is the id of the video capturing device to open.
# To open default camera we enter 0.
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while cam.isOpened():       #isOpened() method checks wheather camera is opened/connected or not.
    ret, frame1 = cam.read()   #Captures image and saves in frame1 and frame2 variables
    ret, frame2 = cam.read()    
    diff = cv2.absdiff(frame1, frame2)  #Shows the difference between two images 
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)   #Converting colored diff picture into gray for sharper image quality
    blur = cv2.GaussianBlur(gray, (5, 5), 0)        #Adding blur effect for better image quality
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) #Adding threshold(Its the the upperlimit upto which we can ignore the movements)
    dilated = cv2.dilate(thresh, None, iterations = 3)  
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #This will draw border around moving objects 
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2) 

    for c in contours:
        if cv2.contourArea(c) < 5000:  #This is for intensity of detection i.e. to ignore minor movements like blinking eye
            continue
        else:
            x, y, w, h = cv2.boundingRect(c)    
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
            #if execution is reached at this point, it is clear that, it has detected a movement
            # So, it will play following .wav file & will call the sendMail() function
            winsound.PlaySound('a.wav', winsound.SND_ASYNC)
            sendMail()
    #If user wants to quit application, he needs to press 'q' 
    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Security Cam', frame1)  #imshow('Window title', 'frame') method to show the frames in the video