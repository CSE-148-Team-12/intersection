# ECE/MAE 148 Team Final Project

## Project Team Members

**Mitchell Herbert** from the CSE department

**Eric Rasmussen** from the MAE department

**Edern Le Goc** from UPS/ext

## Project Overview

We set out to design a program which would have our car autonomously stay in the correct lane and stop at stop signs. Upon stopping at the line, the car would prompt the user for input. Given user input (left, right, or straight), the car would complete the turn autonomously and repeat the process.

Given enough time, we planned on implementing vehicle detection and right-of-way handling.

## Hardware
### Completed Car

![Completed Car](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Car%20Image%201.png)

### Project track

![Project Track](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Track.jpg)

### Camera Mount

![Camera Mount](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Camera_Mount.jpg)

### Acrylic Cut

![Acrylic Cut 1](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Acrylic%20Cut%201.png)

![Acrylic Cut 2](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Acrylic%20Cut%202.png)

### Electrical Schematic

![Electrical Schematic](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Electrical%20Schematic.jpg)

## Software

### Software Overview

Our software had several different main components: 

oakd_control: This file initializes our oakd camera, and sets it to take rgb pictures. It also uses depthai's depth perception code to create a depth map.

line_follower: This section takes in an rgb picture, and then converts it to an HSV format and applies blue/green color masks to it. It then counts the number of blue and green pixels, and finds the difference between the pixel counts to determine steering direction. More green = right, more blue = left. Our code here also must be calibrated to see green and blue in the given lighting. We used an HSV image to filter for the desired color range, so to calibrate the desired color we just need to adjust the SV values in our masks (values set in main.py) and run the code to see if the values are suitable.

vesc_control: This file initializes the VESC, and handles all commands to adjust steering and throttle.

util: Keeps a running average of our VESC steering values.

stop_sign_detector: This code implementes a stop sign detector by the name of CascadeClassifier. Using this detector, it finds and plots the bounding box of our stop sign on our rgb image feed. Then using our previously created depth map, it takes an average depth reading from the center of the bounding box. It then returns this distance value for us to stop our car.

turn_system: After the car has been stopped, this code asks the user which direction it should turn. Then, using preset values for throttle and steering based on direction, it directs the car through the intersection.

main: Initializes all the classes listed above using values that are very easy for us to adjust and tinker with. After initialization, it runs our line following code in a while loop, interrupting the loop at stop signs and resuming it after each intersection is handled.

### Relevant Images

![Stop Sign Detection](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Stop%20Sign%20Detection.png)

![Line Following](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Line%20Following.png)

### How to run

To run our code, use the run.sh file in our repo. We made this file in order to solve an error which said we lacked permission to access the VESC's serial port. This code chmod's the proper file and then automatically runs our main code file.

Please note that our test.sh file is not functional, as it was made to work with an older version of our code which ran off a video for testing.

## Challenges Faced

### Glare

Our greatest issue was line finding with the presence of glare. Glare shows up as almost entirely white, and is nearly impossible to filter when finding white lines. However, when finding greens and blues in an HSV filter, it is possible to filter out glare with extremely specific SV masks. Discovering this, we decided to forgo line finding and to have our car detect greens and blues for steering. 

### Nighttime vs Daytime Lighting

Lighting was also a massive issue as our track was outdoors. Every hour or so the lighting would be different enough that our color filters would begin to break down. At day there would be glare from direct sunlight, while at night there would be glare from the inconsistent ceiling lights and hallway lights.

### Narrow Camera FOV

Another issue was our low camera FOV, which contributed to two problems. Firstly, the camera FOV is so low it can barely see both lane lines on the class track. This made it extremely difficult for us to make a line follow algorithm, and made it so the final track we built had very narrow lanes. Secondly, our FOV was so narrow that we could no longer see stop signs when we stopped at an intersection. It made it impossible to perfectly stop at the intersection line as the sign was out of view. Our solution was to implement a delay, so that it would stop a short time after it saw our stop sign rather than immediately.

### Inaccurate Depth Readings

We also had a problem with accurately measuring distance to the stop sign, as our depth readings were inconsistent. This resulted from two things. For one, the stop signs were made out of paper. If they were bent slightly then the depth reading on that part of the sign would be zero, throwing our measurement off. Secondly, the lighting drastically affected our detection of the stop signs, and if they were poorly lit then they could escape detection altogether. In future we sould need to build sturdier signs, and get better lighting for them.

### VESC Crashes from Large Adjustments

Our VESC also gave us a lot of trouble as it had numerous bugs we did not know how to solve. The greatest challenge it gave us was with steering. If we told our VESC to make a sharp turn change, for example a max left turn to a max right turn, it would crash. Any kind of sudden/large change would make our code completely break. Our solution to this was to have a running average of our last 5-10 steering values, so that whatever value we passed to the VESC could not be extremely different from our last value.

### Canny and HoughLinesP Line Following

Our team spent multiple weeks trying to get line detection from a canny filter and the HoughLinesP function. Though we almost got the method to work, we ultimately abandoned it for green/blue filtering as the method was plagued with errors. Firstly, it would constantly read glare as an erroneous lane line. Secondly, the algorithm would often read lines too far ahead of it, and would turn too early. Third, the finding function itself was highly flawed, and sometimes did not detect lane lines when there were clear ones, and sometimes detected them out of small glare patches. Fourthly, it would also detect the concrete at the edge of the track as a lane line. And lastly, it was nearly impossible to determine steering from a single line as we could never know which side of the line we were on.

### Red-Green Filtering

We also experimented with red-green filtering as blue was difficult to detect in the dark. Though we guess it would ultimately work, there was also other errors it introduced. For instance, our stop signs were also red, and would introduce steering error. Glare is also highly red, so we would have difficulty filtering it out.

### Tiny-Yolo Bounding Boxes

Another problem we had was initially using Tiny-Yolo for stop sign recognition. Tiny-Yolo overall is inefficient and was not good at detecting the signs. Primarily, it split the detection of the stop signs into several different stop signs that we could not use for a depth measurement. We had to average these boxes into one unifed box we could actually take our measurement from, but this process was extremely inaccurate as the boxes themselves were inaccurate. We suspect this was because the stop signs were far larger in our image than what Tiny-Yolo was built for. Sometimes Tiny-Yolo would also detect stop signs off of vaguely octagon shaped objects, and even read a nonexistent stop sign off of a reflection of glass. It also sometimes completely passed our stop signs without detecting anything.

## Project Results

### Demo Video
[Demo Video](https://www.youtube.com/watch?v=1tUkvhMy6k4)

### Results Summary

We successfully completed our objectives. As demonstrated in our video, our car was able to...

1. Stay between the lines
2. Stay in the right lane (mostly)
3. Stop at stop signs
4. Wait for user input
5. Autonomously traverse the intersection

We ran out of time and were unable to implement vehicle detection and right-of-way handling.

### Potential Improvement

Given more time, we would have tested vehicle detection using LIDAR and/or tiny-yolo. Upon getting it working, we would have implemented some algorithm for right-of-way.

We also believe that our current algorithm could be improved by using the white lines on the track to stop correctly. The car did not always stop straight at the line. We could have fixed this by stopping perpendicular to the white line.

## Resources
[GitHub Repository](https://github.com/CSE-148-Team-12/intersection)

[Project Update Presentation](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/ECE%20148%20Team%2012%20Final%20Presentation%2012_8_2022.pdf)

[Final Presentation](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/ECE%20148%20Team%2012%20Final%20Presentation%2012_8_2022.pdf)

[Demo Video](https://www.youtube.com/watch?v=1tUkvhMy6k4)

