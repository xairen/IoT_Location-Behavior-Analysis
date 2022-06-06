# Analysis of behavioral patterns using rotary sensor & location

Project Description : 

Personal devices or mobiles phones have become an intangible part of human lives. They come in handy and can be utilized to obtain data which can allow us to perform various analyses to identify behavioral patterns in users. This study will be divided into two main functionalities. In the first one, the angle at which the device is being kept at will be utilized to identify whether the device is being used or is idle. For example, when the mobile device is kept at a 180 degree angle we can safely assume that the device is either being charged or is kept somewhere while the user is sleeping. The main assumption is that the user always carries his phone everywhere. For each angle it is kept at we will be able to collect useful insights. As for the second functionality, utilizing the Geolocation API analyses of the end user’s location will be done. These two insights will be clubbed together and analyzed to comment on the routine or pattern of the end-user. Other parameters such as gyroscope and accelerometer can be utilized to obtain more accurate data about the usage of the device.  

Flow:

![image](https://user-images.githubusercontent.com/92839740/172246895-b71a9c90-709f-49b9-901f-14c20e51f61e.png)

List of tools used : 

1. IoT device (Omega 2) with arduino board
3. Rotary sensor
4. AWS IoT
5. Geolocation API

Step by Step instruction of Project :

Step 1: Unzip the files from folder 

Step 2: Connect rotary sensor to A1 (Arduino board)

Step 3: Connect the laptop to the Omega

Step 4: Copy paste the python code(main.py) to the root folder in Omega along with the AWS certificates

Step 5: Upload the Arduino code (rot-angle.ino)

Step 6: Open MQTT Client in AWS

	Subscribe to topic - # 

	Subscribe to topic - Omega_0000/+/details

Step 7: Run the python code in Omega terminal using “python3 main.py”

Step 8: If the rotary angle lies in between 89 and 100 then enter one of these address 

1) 	Rochester, New York
2)	Rochester, Monroe, New York
3)	Rochester, Brooks Ave, New York
4)	Rochester, Henrietta, New York

Note: You can enter any address and it will provide you with the latitude and longitude of the address you have inputted but I have specified specific locations for the 3 instances (Address1, Address2, Address3)

If the angle is 0 then it will display message that the device is on charge or not in use. Else it will display message that the device is in use and calculate the amount of time spent on device. Since the device in this case is the Omega the amount of time is in seconds.

