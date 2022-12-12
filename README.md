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

### Acrylic Cut

![Acrylic Cut 1](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Acrylic%20Cut%201.png)

![Acrylic Cut 2](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Acrylic%20Cut%202.png)

### Electrical Schematic

![Electrical Schematic](https://github.com/CSE-148-Team-12/intersection/blob/main/Resources/Electrical%20Schematic.jpg)

## Software

### Software Overview

### Relevant Images

### How to run


## Challenges Faced

### Glare

### Nighttime vs Daytime Lighting

### Narrow Camera FOV

### Inaccurate Depth Readings

### VESC Crashes from Large Adjustments

### Canny and HoughLinesP Line Following

### Red-Green Filtering

### Tiny-Yolo Bounding Boxes


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

