# AudioPulse Capstone Project Report

## Part 1: Audio Download Pipeline & Logging
The goal of Part 1 is to create a working pipeline that downloads audio from a list of Youtube URLs, extracts the metadata, and logs the process. This has been done in two ways, a serial way and a parallel way. 

### Pipeline


### Serial vs Parallel
The assesment asked to do two different process to download the data, one serial and one parllel extracting 5 songs at the time. I did that and also I wanted to try to extract all of the information at once. 
There is a massive time difference, ofc this changes every time but more or less the serial one will take about 50 to 60 seconds while the parallel process takes 2 to 4 seconds and the one wiht a semaphore will take 5 to 6 seconds. 

The positive notes about the serial approach would be that ise reliable and simpler so is an easier code to code and to explain. But its slow, in this scenario we are only looking into 10 to 15 songs and it takes that much, but if we wanted to use bigger amounts of data it will not be an option.

The parallel programming on the other hand is more complex to program and if there is an error on the process i thing is more difficult to know where the problem is. The good things about this is that is faster and more scalable.

## Part 2: Audio Data Extraction

## Part 3: Data Analysis

