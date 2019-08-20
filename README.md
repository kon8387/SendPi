**ST0324 Internet of Things CA2 Step-by-step Tutorial**

# IOT CA2 Temperature Buddy
### By SendPi

# Step-By-Step Tutorial


## Table of Contents

* Overview
* Final RPI set-up
* Hardware Requirements
* Hardware Setup
* AWS Cloud Setup
  - Create AWS Thing
  - EC2 Web Application
  - DynamoDB Setup
* Raspberry pi Setup
  - Node-Red
* Running the Project
* Video
* Appendix: node_red_diagram


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

- Login to your aws account, click on aws console and using the serach function search for the IoT core module and click get started.

![](https://github.com/kon8387/SendPi/blob/master/img/10.png)

- On the left side panel look for the tab Manage, next click things

![](https://github.com/kon8387/SendPi/blob/master/img/11.png)

- Click on create and select create a single thing

![](https://github.com/kon8387/SendPi/blob/master/img/12.png)

- Enter the name for your device and leave everything else on default
![](https://github.com/kon8387/SendPi/blob/master/img/13.png)

- Next, click on the first option, Create certificate. Downnload all the 4 files.

- For the root CA file download the RSA 2048, VeriSign Class 3 public primary G5 root CA certificate option. Right click and save the key as rootca.perm. Click activate to activate the certificate.

![](https://github.com/kon8387/SendPi/blob/master/img/14.png)

![](https://github.com/kon8387/SendPi/blob/master/img/15.png)

- Rename the 4 files to these filenames

![](https://github.com/kon8387/SendPi/blob/master/img/16.png)

- We will use these files later on in the Setup

- After clicking Activate Certificate, Next click attach policy, leave it blank for now and click register to register your thing.

- On the left dashboard, select policies under the secure sub-menu
Choose Create New policy

- On the create a policy page key in the

|Variable       |  Value    |
|---------------|-----------|
|Name:          | PolicyName|
|Action:        |  iot:*    |
|Resource ARN:  | *         |

- Ensure the "allow" tick box is checked

![](https://github.com/kon8387/SendPi/blob/master/img/17.png)

- Click on Create the Policy

- Going back to the left Dashboard, Click ceritificates under the security sub-menu

- Click on the checkbox besides the certificate we created and select the action button on the top right. Click on attach Policy

![](https://github.com/kon8387/SendPi/blob/master/img/18.png)

- Select the policy you created and click on attach to attach this policy to the certificate

- Again Click on the checkbox besides the certificate we created and select the action button on the top right. Click on attach thing

![](https://github.com/kon8387/SendPi/blob/master/img/18.png)

- Select the thing we created and click attach to attach the certificate to our thing

- Go back to the Manage > things sub-menu and chose the thing we created

- On the left sub panel select interact, we will be shown the thing’s endpoint

![](https://github.com/kon8387/SendPi/blob/master/img/19.png)

- Copy down this value and replace the endpoint values in the server.py,dht.py and node-red MQTT input configuration (Shown in Node-Red setup).


### EC2 Web Application setup

- In the aws console, create an EC2 instance and select “amazon linux AMI”

![](https://github.com/kon8387/SendPi/blob/master/img/20.png)

- Then follow the settings below for instance type and security group.

![](https://github.com/kon8387/SendPi/blob/master/img/21.png)

![](https://github.com/kon8387/SendPi/blob/master/img/22.png)

- Click launch and choose to create a new key-pair. Save this file

![](https://github.com/kon8387/SendPi/blob/master/img/23.png)

- Then, to access EC2, you would need download and use these programs
1. Putty to ssh into EC2 instance
2. Puttygen to generate private public key, used for putty and scp
3. Winscp to transfer files to the EC2

- Open puttygen and load the keyfile and click the “save private key” option. This will be a .ppk file

![](https://github.com/kon8387/SendPi/blob/master/img/24.png)

- Then, using putty, you can use the host name “ec2-user@**ec2 dns**” where **ec2 dns** is the public dns provided in the EC2 console.

![](https://github.com/kon8387/SendPi/blob/master/img/25.png)

- Then, specify the key file which would be the .ppk file gotten previously

![](https://github.com/kon8387/SendPi/blob/master/img/26.png)

- Now you can log into the EC2 machine

- To transfer files over to EC2, you can use WinSCP. Specify the host name as the DNS provided by EC2 and the username as “ec2-user”. Then you can proceed to transfer files

![](https://github.com/kon8387/SendPi/blob/master/img/27.png)

- You can now move the “web server” folder into EC2.

![](https://github.com/kon8387/SendPi/blob/master/img/28.png)

- Opening up the web folder we have to edit the server.py file.The credentals and host needed for dynamodb are hardcoded into server.py. Please change these values to your own accounts values.

- You can find your credential info by looking into the aws site and clicking account details

![](https://github.com/kon8387/SendPi/blob/master/img/10.png)

- Click show CLI to see the crendtials information, copy this credentials information and change it in the hardcoded server.py.Take note of the credentials, it will be used again in the Raspberry pi Setup

![](https://github.com/kon8387/SendPi/blob/master/img/29.png)

- Transfer the certificate.perm.crt, private.pem.key,rootca.perm into the webfolder.Ensure that you have the needed certificate files in the same file level with your server.py

![](https://github.com/kon8387/SendPi/blob/master/img/30.png)

- Install the necessary modules onto EC2 using putty's command line
`sudo  pip install boto3, AWSIoTPythonSDK,gevent,paho-mqtt,numpy,flask`

- Now you can start up the server, using putty which is still connected, run
`sudo python server.py`

![](https://github.com/kon8387/SendPi/blob/master/img/31.png)

- Use your web browser and go to the public ipv4 address provided by EC2 and you should see the web application

![](https://github.com/kon8387/SendPi/blob/master/img/32.png)


### DynamoDB setup
- In the AWS Console,go to AWS DynamoDB and create a table with the keys “deviceid” and “datetimeid”

![](https://github.com/kon8387/SendPi/blob/master/img/33.png)

- Once you successfully run dht.py on your raspberry pi, the dynamodb will automatically have the temperature and humidity column.

![](https://github.com/kon8387/SendPi/blob/master/img/34.png)


### Raspberry Pi Setup
- First connect the hardware as seen in the Hardware setup section


- Install the necessary modules
`sudo  pip install boto3, AWSIoTPythonSDK,gevent,paho-mqtt,numpy`

- Run the command `aws configure` and paste in the aws credentals into your aws account.

- Move the folder pi into your raspberry pi

- Move your various AWS certificate files into the folder

- Ensure that you have the various certificate files in the same level as your dht.py

![](https://github.com/kon8387/SendPi/blob/master/img/35.png)

- Next import the node_red_diagram.txt into node red. **An additional copy** is uploaded as apendix on the last segment of this readme

![](https://github.com/kon8387/SendPi/blob/master/img/36.png)

- Enusre the diagram looks like this(refer below)

![](https://github.com/kon8387/SendPi/blob/master/img/37.png)

- Double click the MQTT node

![](https://github.com/kon8387/SendPi/blob/master/img/38.png)

- Click the edit icon next to the server

![](https://github.com/kon8387/SendPi/blob/master/img/39.png)

- Enter your AWS endpoint in the server text box, then click the edit icon in the TLS configuration

![](https://github.com/kon8387/SendPi/blob/master/img/40.png)

- Change the Credentials to your 3 credential files in the mqtt function and test the connection

![](https://github.com/kon8387/SendPi/blob/master/img/41.png)

- Deploy the node_red_diagram to recieve MQTT messages to turn the LED ON/OFF

#### That concludes the setup for this porject

### Running the project
###### To run the Project

- On your various raspberry pi, launch node-red and deploy the configured flow diagram

![](https://github.com/kon8387/SendPi/blob/master/img/37.png)

- Next change directory to where the dht.py is stored and run the dht.py to read input from the DHT sensor and insert to the AWS dynamo db.
`python dht.py`
\*Disclaimer try running without sudo if there is an exception or refreshing your AWS credential information

![](https://github.com/kon8387/SendPi/blob/master/img/34.png)

- Next using putty, establish a connection to your AWS EC2 instance.


- Run the server.py
`sudo python server.py`
\*Disclaimer try running without sudo if there is an exception or refreshing your AWS credential information

- Navigate to your EC2’s public IPV4 address and the web application should be deployed.

![](https://github.com/kon8387/SendPi/blob/master/img/32.png)

## Video

### Link: https://youtu.be/HrpM4NIARHs

<a href="http://www.youtube.com/watch?feature=player_embedded&v=HrpM4NIARHs
" target="_blank"><img src="https://github.com/kon8387/SendPi/blob/master/img/youtube.png"
alt="IMAGE ALT TEXT HERE" width="90%" height="" border="2" align="center" /></a>


### Apendix: node_red_diagram
`[{"id":"9fccd953.ee6208","type":"tab","label":"Flow 2","disabled":false,"info":""},{"id":"265a05aa.f09ada","type":"mqtt in","z":"9fccd953.ee6208","name":"aws-mqtt","topic":"sensor/light","qos":"1","datatype":"auto","broker":"9c1053a0.adb01","x":170,"y":120,"wires":[["7805f6c9.f36c58","4b4f0817.712a58"]]},{"id":"7805f6c9.f36c58","type":"debug","z":"9fccd953.ee6208","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":360,"y":60,"wires":[]},{"id":"ae7ac585.49d278","type":"rpi-gpio out","z":"9fccd953.ee6208","name":"led","pin":"12","set":true,"level":"0","freq":"","out":"out","x":570,"y":180,"wires":[]},{"id":"4b4f0817.712a58","type":"function","z":"9fccd953.ee6208","name":"check payload","func":"if (msg.payload == 'on'){\n    msg.payload = 1\n}\nelse{\n    msg.payload = 0\n}\nreturn msg;","outputs":1,"noerr":0,"x":370,"y":180,"wires":[["ae7ac585.49d278","474659e6.b4e078"]]},{"id":"474659e6.b4e078","type":"debug","z":"9fccd953.ee6208","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","x":440,"y":300,"wires":[]},{"id":"9c1053a0.adb01","type":"mqtt-broker","z":"","name":"aws-hc","broker":"a2gdmm3ooqtbpf-ats.iot.us-east-1.amazonaws.com","port":"8883","tls":"3856b5ab.3a3eba","clientid":"ken8387","usetls":true,"compatmode":true,"keepalive":"60","cleansession":true,"birthTopic":"","birthQos":"0","birthPayload":"","closeTopic":"","closeQos":"0","closePayload":"","willTopic":"","willQos":"0","willPayload":""},{"id":"3856b5ab.3a3eba","type":"tls-config","z":"","name":"hc","cert":"/home/pi/CA2/certificate.pem.crt","key":"/home/pi/CA2/private.pem.key","ca":"/home/pi/CA2/rootca.pem","certname":"","keyname":"","caname":"","servername":"","verifyservercert":true}]`
