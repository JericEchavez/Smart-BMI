from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import math

import time
import sys

import os
import bisect





################################
# Measure Weight
################################

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(23038) #-7846.82

hx.reset()
hx.tare()
print("Add weight now...")





weightCounter = 0
processing = False

while True:
    while True:
        try:
            val = abs(hx.get_weight(5))
        
            hx.power_down()
            hx.power_up()
            time.sleep(1)
            if val < 10:
                # Title Screen
                cv2.namedWindow("window", cv2.WINDOW_NORMAL);
                cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

                photo = cv2.imread('Screen/smartBmi.png')
                cv2.imshow("window", photo)
                key = cv2.waitKey(1) 
                
            elif val > 10:
                #print(val)
                weightCounter += 1
                if processing == False:
                    print('Processing....')
                    processing = True
                    print(weightCounter)
                    
                    cv2.namedWindow("window", cv2.WINDOW_NORMAL);
                    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

                    photo = cv2.imread('Screen/processing.png')
                    cv2.imshow("window", photo)
                    key = cv2.waitKey(2)
                print(weightCounter)
            else:
                print('.')
                
            if weightCounter == 5:
                weightCounter = 0
                break
            
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
    
    print("\nYour Weight is: ",round(val,2))
    #val = int(val)
    processing = False




    ################################
    # Measure Height
    ################################
    isHeightValid = False

    while True:
        if isHeightValid == False:
            key = cv2. waitKey(2)
            webcam = cv2.VideoCapture(0)
            webcam.set(3, 1280)  
            webcam.set(4, 960)
            webcam.set(cv2.CAP_PROP_AUTOFOCUS, 0)

            check, frame = webcam.read()
            print(check) #prints true as long as the webcam is running
            print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(2)
               
             
               
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()

            img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
            img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(50)
            cv2.destroyAllWindows()

            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            img_resized = cv2.imwrite(filename='example_02.jpg', img=img_)
            print("Image saved!")




                    
            # Function to show array of images (intermediate results)
            def show_images(images):
                for i, img in enumerate(images):
                    cv2.imshow("image_" + str(i), img)
                cv2.waitKey(2)
                cv2.destroyAllWindows()

            img_path = "example_02.jpg"

            # Read image and preprocess
            image = cv2.imread(img_path)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (9, 9), 2)

            edged = cv2.Canny(blur, 100, 100)
            edged = cv2.dilate(edged, None, iterations=1)
            edged = cv2.erode(edged, None, iterations=1)

            #show_images([blur, edged])

            # Find contours
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Sort contours from left to righeight as leftmost contour is reference object
            (cnts, _) = contours.sort_contours(cnts)

            # Remove contours which are not large enough
            cnts = [x for x in cnts if cv2.contourArea(x) > 150]

            #cv2.drawContours(image, cnts, -1, (0,255,0), 2)

            #show_images([image, edged])
            #print(len(cnts))

            # Reference object dimensions
            # Here for reference I have used a 2cm x 2cm square
            ref_object = cnts[0]
            box = cv2.minAreaRect(ref_object)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            dist_in_pixel = euclidean(tl, tr)
            dist_in_cm = 19.1
            pixel_per_cm = dist_in_pixel/dist_in_cm



            userHeight = 0

            # Draw remaining contours

            for cnt in cnts:
                
                box = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                (tl, tr, br, bl) = box
                
                #x,y,w,h = cv2.boundingRect(cnt)
                #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

                cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
                mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0])/2), tr[1] + int(abs(tr[1] - br[1])/2)) 

                height = euclidean(tr, br)/pixel_per_cm
                cv2.putText(image, "{:.1f}cm".format(height), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                

                #this will assign the value of height of the person
                if height > 80:
                    userHeight = height


        #show_images([image])
        print('weight: ', round(val,1))
        print('height: ', round(userHeight, 1))
        if userHeight < 100:
            isHeightValid = False
        else:
            cv2.imwrite(filename='final.jpg', img=image)
            cv2.namedWindow("window", cv2.WINDOW_NORMAL);
            cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
            photo = cv2.imread('final.jpg')
            key = cv2.waitKey(2)
            cv2.imshow("window", photo)
            key = cv2.waitKey(2)
            
            process = 0
            for x in range (4):
                process+=1
                time.sleep(1)
                if process == 3:
                    cv2.destroyAllWindows()
                    break
            break
            





    ################################
    # BMI
    ################################
    underweight = False
    normal = False
    overweight = False
    obese = False
    
    
    
    
    f_Weight = round(val, 1)
    f_Height = round(userHeight,1)
    
    heightInMeters = f_Height/100
    squared = heightInMeters*heightInMeters
    
    f_Bmi = f_Weight/squared
    s_Suggestion = ""
    
    bmiCategoryList = ["Underweight", "Normal", "Overweight", "Obese"]
    bmiNumbers = [18.4, 24.9, 29.9]
    s_BmiCategory = bmiCategoryList[bisect.bisect_left(bmiNumbers,f_Bmi)]

    print("Your BMI is: ",round(f_Bmi,1),"Kg/m2. That means",s_BmiCategory)

    #Suggestions
    if s_BmiCategory == "Underweight":
        s_Suggestion = "When you are underweight, you may feel full faster. Eat five to six smaller meals during the day rather than two or three large meals. Choose whole-grain breads, pastas and cereals, fruits and vegetables, dairy products, lean protein sources, and nuts and seeds.Try cardiovascular exercise for 20mins - jumping jack, jog in place, squat jumps, staircase exercise, and running."
        underweight = True
                
    elif s_BmiCategory == "Normal":
        s_Suggestion = "You are in the recommended weight range for your height. But your health may still be at risk if you are not getting regular physical activity (jumping jack, jog in place, squat jumps, stair case exercise, and running) and practicing healthy eating. "
        normal = True
    
    elif s_BmiCategory == "Overweight":
        s_Suggestion = "Start your day with a high-protein meal especially warm, solid food helps you feel fuller and less hungry later. Shoot for 350-400 calories with at least 25 grams of protein. Focus on activities that put minimal stress on your joints, like walking, swimming, or water exercises. Your goal should be to get 30 minutes of exercise a day, five days a week."
        overweight = True
    
    else:
        s_Suggestion = "Avoid from eating or drinking foods, such as sugar sweetened beverages, fruit juice, refined grains, Other highly processed foods, such as fast food 5-6 days of cardio performed at least twice a day that adds up to 60 minutes per day. Cardio Activities Include walking, jogging, biking or anything else you can think of to keep you moving."
        obese = True
    
    s_Height = str(f_Height)  # float to string conversion
    s_Weight = str(f_Weight)
    s_Bmi = str(round(f_Bmi,1))
    
    
    os.system("sudo chmod a+w /dev/usb/lp0")
    os.system("sudo echo -e '\n\n\nSmart BMI \n\nHeight: " +s_Height+ " cm\nWeight: " +s_Weight+ " kg\nBMI: " +s_Bmi+ " kg/m2\nBMI Category: " +s_BmiCategory+ "\n\n\nSuggested Diet: \n\n"+s_Suggestion+"\n\n\n\n\n\n' > /dev/usb/lp0")
    #time.sleep(5)
    
    if underweight == True:  
        cv2.namedWindow("window", cv2.WINDOW_NORMAL);
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

        photo = cv2.imread('Screen/underweight.png')
        cv2.imshow("window", photo)
        key = cv2.waitKey(2)

        process = 0
        for x in range (8):
            process+=1
            time.sleep(1)
            if process == 7:
                cv2.destroyAllWindows()
                break
    
    elif normal == True:  
        cv2.namedWindow("window", cv2.WINDOW_NORMAL);
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

        photo = cv2.imread('Screen/normal.png')
        cv2.imshow("window", photo)
        key = cv2.waitKey(2)

        process = 0
        for x in range (8):
            process+=1
            time.sleep(1)
            if process == 7:
                cv2.destroyAllWindows()
                break
    
    elif overweight == True:  
        cv2.namedWindow("window", cv2.WINDOW_NORMAL);
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

        photo = cv2.imread('Screen/overweight.png')
        cv2.imshow("window", photo)
        key = cv2.waitKey(2)

        process = 0
        for x in range (8):
            process+=1
            time.sleep(1)
            if process == 7:
                cv2.destroyAllWindows()
                break
    
    else:  
        cv2.namedWindow("window", cv2.WINDOW_NORMAL);
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

        photo = cv2.imread('Screen/obese.png')
        cv2.imshow("window", photo)
        key = cv2.waitKey(2)

        process = 0
        for x in range (8):
            process+=1
            time.sleep(1)
            if process == 7:
                cv2.destroyAllWindows()
                break