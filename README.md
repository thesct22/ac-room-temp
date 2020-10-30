# ac-room-temp

The Python code reads data from a csv file which has data of initial temperature preference, final temperature preference and time interval between setting these two values by the system.
roomtemp.ino is for reading room temperature by NodeMCU and sending to RPi using MQTT
actemp.ino is for setting temperature value to AC as per temperature value sent by RPi to it.
