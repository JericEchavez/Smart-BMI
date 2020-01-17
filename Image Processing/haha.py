import bisect

#! /usr/bin/python2

import time
import sys

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

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
#hx.set_reference_unit(400)
hx.set_reference_unit(483)

#hx.reset()

#hx.tare()

#print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

#while True:
for i in range(10):
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = (hx.get_weight(5))/38
        print((val))
        #print((val))

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


######  BMI  #######
gender = input("Are you a male(m) or female(f): ")
age = int(input("How old are you: "))
weight = val
height = float(input("What is your height in centimeters: "))

bmi = round(weight / ((height/100) ** 2))

if age < 19:
    print("You're too young for this and I'm concerned you may be at risk of developing an eating disorder.")
    exit()

optimal_bmi_range_min_ages = [25, 35, 45, 55, 65]
optimal_bmi_ranges = [(19, 24), (20, 25), (21, 26), (22, 27), (23, 28), (24, 29)]
optimal_bmi_range = optimal_bmi_ranges[bisect.bisect_left(optimal_bmi_range_min_ages, age)]

if bmi >= optimal_bmi_range[0] and bmi <= optimal_bmi_range[1]:
    print("Your BMI is optimal for your age!")
else:
    print("Your BMI is not okay for your age!")

bmi_categories = ["underweight", "normal weight", "overweight", "obesity", "strong obesity"]
if gender == "m":
    bmi_cat_thresholds = [19, 26, 31, 41]
elif gender == "f":
    bmi_cat_thresholds = [18, 25, 31, 41]
else:
    print("Your BMI is",bmi)
    exit()

bmi_category = bmi_categories[bisect.bisect_left(bmi_cat_thresholds,bmi)]
print("Your BMI is " + str(bmi) + " Kg/m2. That means " + bmi_category)

#####  PRINT  #####
#print(val)

import os
os.system("sudo chmod a+w /dev/usb/lp0")

#f_Height = 0
##f_Weight = 50
#f_Bmi = 0
#s_Obesity = "Undefined"
if gender=='m':
    s_Gender = 'Male'
else:
    s_Gender = 'Female'
    
s_Age = str(age)
#s_Gender = str (gender)
s_Height = str(height)  # float to string conversion
s_Weight = str(round(weight))
s_Bmi = str(bmi)
s_Obesity = str(bmi_category)

os.system("sudo echo -e '\n\n\nSmart BMI \n\nAge: " +s_Age+ "\nGender: " +s_Gender+ "\nHeight: " +s_Height+ " cm\nWeight: " +s_Weight+ " kg\n\nBMI: " +s_Bmi+ "\nThat means you are " +s_Obesity+ "\n\n\n\n\n\n' > /dev/usb/lp0")



