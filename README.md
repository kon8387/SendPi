**ST0324 Internet of Things CA2 Step-by-step Tutorial**

# IOT CA2 Temperature Buddy
### By SendPi

# Step-By-Step Tutorial


## Table of Contents

* Overview
* Final RPI set-up
* Hardware Requirements
* Hardware Setup
* Cloud Setup
  - Create AWS Thing
  - EC2 Web Application
  - DynamoDB Setup
* Raspberry pi Setup
  - Node-Red
* Running the Project
* Video


## Overview of Temperature Buddy

### What is Temperature Buddy about?

Temperature Buddy is a smart room project showcase. It has features like being able to monitor remotely via a responsive web portal,Led lights, temperature and humidity values of each room in the house.

## The final RPI set-up
#### Final Set-up

![](https://github.com/kon8387/SendPi/blob/master/img/1.png)

#### Fritz Diagram
![](https://github.com/kon8387/SendPi/blob/master/img/2.png)

#### System Architecture Design
![](https://github.com/kon8387/SendPi/blob/master/img/3.png)

#### Web Application
![](https://github.com/kon8387/SendPi/blob/master/img/4.png)


## Hardware Requirements

#### 2 DHT11 Sensor
We make use of DHT11 sensors to record the room's temperature and humidity readings. This sensor should used with a 220 Ω Resistor.

![](https://github.com/kon8387/SendPi/blob/master/img/5.png)

#### 2 LED
LED have a logner and shorter leg, the longer leg should be connected to the positive power supply (GPIO 12) and the shorter leg should be connected to ground through a 10K Ω Resistor.

![](https://github.com/kon8387/SendPi/blob/master/img/6.png)

#### 4 Resistor (2 x 220 Ω Resistor, 2 x 10k Ω Resistor)
Resistors help limt the current being drawn from the Raspberry Pi to the connected componennts so as to not draw to much power and cause damage to the Pi.

220 Ω Resistor should be used for our DHT11 sensor

![](https://github.com/kon8387/SendPi/blob/master/img/7.png)

10k Ω Resistor should be used for our LED as they tend to draw alot of power.

![](https://github.com/kon8387/SendPi/blob/master/img/8.png)

## Hardware Setup

#### Fritz Diagram
Congiure the hardware componennts accordingly to the Fritz Diagram shown below

![](https://github.com/kon8387/SendPi/blob/master/img/2.png)

It should look something like

![](https://github.com/kon8387/SendPi/blob/master/img/1.png)


## AWS Cloud Setup

This project requires the setup of AWS dynamodb,IoT Core and EC2

![](https://github.com/kon8387/SendPi/blob/master/img/9.png)

### IoT Core setup

Login to your aws account, click on aws console and using the serach function search for the IoT core module and click get started.

![](https://github.com/kon8387/SendPi/blob/master/img/10.png)

On the left side panel look for the tab Manage, next click things

![](https://github.com/kon8387/SendPi/blob/master/img/11.png)

click on create and select create a single thing

![](https://github.com/kon8387/SendPi/blob/master/img/12.png)

Enter the name for your device and leave everything else on default
![](https://github.com/kon8387/SendPi/blob/master/img/13.png)

Next, click on the first option, Create certificate. Downnload all the 4 files.

For the root CA file download the RSA 2048, VeriSign Class 3 public primary G5 root CA certificate option. Right click and save the key as rootca.perm. Click activate to activate the certificate.

![](https://github.com/kon8387/SendPi/blob/master/img/14.png)

![](https://github.com/kon8387/SendPi/blob/master/img/15.png)

Rename the 4 files to these filenames

![](https://github.com/kon8387/SendPi/blob/master/img/16.png)

We will use these files later on in the Setup

After clicking Activate Certificate, Next click attach policy, leave it blank for now and click register to register your thing.

On the left dashboard, select policies under the secure sub-menu
Choose Create New policy

On the create a policy page key in the

|Variable       |  Value    |
|---------------|-----------|
|Name:          | PolicyName|
|Action:        |  iot:*    |
|Resource ARN:  | *         |

Ensure the "allow" tick box is checked

![](https://github.com/kon8387/SendPi/blob/master/img/17.png)

Click on Create the Policy

Going back to the left Dashboard, Click ceritificates under the security sub-menu

Click on the checkbox besides the certificate we created and select the action button on the top right. Click on attach Policy

![](https://github.com/kon8387/SendPi/blob/master/img/18.png)

Select the policy you created and click on attach to attach this policy to the certificate

Again Click on the checkbox besides the certificate we created and select the action button on the top right. Click on attach thing

![](https://github.com/kon8387/SendPi/blob/master/img/18.png)

Select the thing we created and click attach to attach the thing certificate to our thing

Go back to the Manage > things sub-menu and chose the thing we created

On the left sub panel select interact, we will be shown the thing’s endpoint

![](https://github.com/kon8387/SendPi/blob/master/img/19.png)

Copy down this value and replace the endpoint values in the server.py,dht.py and node-red MQTT input configuration (Shown in Node-Red setup). 


### EC2 Web Application setup

In the aws console, create an EC2 instance and select “amazon linux AMI”

![](https://github.com/kon8387/SendPi/blob/master/img/20.png)

Then follow the settings below for instance type and security group.

![](https://github.com/kon8387/SendPi/blob/master/img/21.png)

![](https://github.com/kon8387/SendPi/blob/master/img/22.png)
