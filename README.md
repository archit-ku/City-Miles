# Transit-Tracker

Submission to Virtual Global Hackathon for team Tangerine Alert

This code is written in Python purely as it's easy to develop iterations of the proof of concept. The production code for this is designed to run using more advanced frameworks and technologies for efficiency and performance. More details on these technologies can be found in our brief.

The program will require input of grid references to locations in UberLand. In production, this input would come via RFID on arbitrary kiosks and scanners, but for testing will simply be inputs in the form "[xCoord], [yCoord]" with a range from 0 to 1000 for each value.

The program will create 2 files. startCoordStorage.txt holds the coordinates of the scanner where you start a journey. This ensures your journey isn't cleared if you close the program during your journey. totalRewards.txt holds a running total of all the points in a user's name. Both files should be encrypted. The latter should be editable by another program with a password input, such that it can be deducted from when redeeming award points. The former should only be editable within this script.
