# SentimentStar
A home project with the goal of gaining useful and demonstrable practical experience in Apache Kafka and ksql for data stream processing

I conducted a home project with the goal of gaining useful and demonstrable practical experience in Apache Kafka and ksql for data stream processing - a modern approach to data integration particularly valuable for today's world of high data volumes and continuous streams of events.

#IoT #Kafka #RaspberryPi #Node-RED #StreamProcessing #EventDrivenArchitecture #Cognitive #OpenSource #SentimentAnalysis #RealTime #BigData #MQTT

I built a Node-RED application on a Raspberry Pi using a Twitter developer account to receive and classify tweets on the topics of Brexit, Covid and Christmas in real-time. Having installed the open source Confluent platform, I produced the stream of classified tweets to a Kafka topic. Using ksql within Kafka I aggregated the data to count the messages per class in continuous 30 second windows. I consumed this data from a Kafka topic back into Node-RED and implemented some processing to maintain the most popular topic of the last 30s. I implemented a multi-threaded Python app on a Raspberry Pi to call APIs to retrieve the most popular topic, to control the LED pattern of a connected Christmas Star hung on my Christmas tree. This allows a non-intrusive IoT device - the Star - to be both decorative and an indicator of real-time public sentiment.

For a photo see https://twitter.com/jonmaddison/status/1338543901817311235
