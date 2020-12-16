# SentimentStar
A home project with the goal of gaining useful and demonstrable practical experience in Apache Kafka and ksql for data stream processing

I conducted a home project with the goal of gaining useful and demonstrable practical experience in Apache Kafka and ksql for data stream processing - a modern approach to data integration particularly valuable for today's world of high data volumes and continuous streams of events.

#IoT #Kafka #RaspberryPi #Node-RED #StreamProcessing #EventDrivenArchitecture #Cognitive #OpenSource #SentimentAnalysis #RealTime #BigData #MQTT

I built a Node-RED application on a Raspberry Pi using a Twitter developer account to receive and classify tweets on the topics of Brexit, Covid and Christmas in real-time. Having installed the open source Confluent platform, I produced the stream of classified tweets to a Kafka topic. Using ksql within Kafka I aggregated the data to count the messages per class in continuous 30 second windows. I consumed this data from a Kafka topic back into Node-RED and implemented some processing to maintain the most popular topic of the last 30s. I implemented a multi-threaded Python app on a Raspberry Pi to call APIs to retrieve the most popular topic, to control the LED pattern of a connected Christmas Star hung on my Christmas tree. This allows a non-intrusive IoT device - the Star - to be both decorative and an indicator of real-time public sentiment. 

Here's the star: https://thepihut.com/products/raspberry-pi-christmas-tree-star

For a photo of it installed: https://twitter.com/jonmaddison/status/1338543901817311235

For Kafka, I installed the Confluent Platform Community Components edition from https://www.confluent.io/download/ onto my Mac on my home network. 

Node-RED and the Python app (code attached) are both running on a local Raspberry Pi Zero - that which is hanging off my Christmas tree with the Star attached.

The Node-RED flow is attached.  View the raw content and import it into Node-RED from the clipboard.
- this requries a Twitter account with a developer account (http://developer.twitter.com) to obtain the desired credentials for the Twitter input node.  This uses https://flows.nodered.org/node/node-red-node-twitter  
- the Kafka producer/consumer nodes require the hostname of the Kafka cluster.  This uses https://flows.nodered.org/node/node-red-contrib-kafka-client
- there is also a hook to set the 'power' as 'on' or 'off', via MQTT.  I have done this by responding to 'Alexa, turn star on/off' commands over MQTT - via Alexa Home Skill Bridge (https://alexa-node-red.bm.hardill.me.uk) and Node-RED running on the IBM Watson IoT Platform - as I happen to have an instance running there, with the Alexa Home Bridge already set up.
- this produces data to a kafka topic called 'nodered, which gets created automatically.  There is also a 'helloworld' test in the flow to confirm Kafka connectivity.

The Python source code is already attached.  This has two threads, sharing global variables (probably a lazy way to do it).
- thread 1: polls the Node-RED API running locally to get 'power' and the 'lastWindowMostPopular' tweet topic.
- main thread: sets the star LED pattern based on the most popular topic, or turns lights off on the star if power is 'off'. 

My python app used code from https://github.com/modmypi/Programmable-Christmas-Star as the basis.

Kafka has just two ksql commands - a stream and a table, created as persistent querirs that run continuously:
- To create a stream representing the 'nodered' topics written to by Node-RED:
ksql> create stream nodered (tweettime int, tweetclass varchar) with (kafka_topic='nodered', value_format='JSON');

- To aggregate the data into 30 second windows:
ksql> create table tweetsperperiod as select tweetclass, count(tweetclass) as count from nodered window tumbling (size 30 seconds) group by tweetclass;
This creates a tweetsperperiod topic that is consumed back into Node-RED.  Note that every update to this topic is continuously consumed so Node-RED needs to keep track of the highest count per topic, per window. 
