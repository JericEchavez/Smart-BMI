import os
#os.system("sudo chmod a+w /dev/usb/lp0")

f_Height = 5.6
f_Weight = 50
f_Bmi = 20.42
s_Obesity = "Normal"

s_Height = str(f_Height)  # float to string conversion
s_Weight = str(f_Weight)
s_Bmi = str(f_Bmi)

os.system("sudo echo -e '\n\n\nSmart BMI \n\nHeight: " +s_Height+ "\nWeight: " +s_Weight+ "\nBMI: " +s_Bmi+ "\nObesity Level: " +s_Obesity+ "\n\n\n' > /dev/usb/lp0")
