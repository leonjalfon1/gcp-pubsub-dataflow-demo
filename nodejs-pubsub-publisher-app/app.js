var express = require('express');
var app = express();
require('log-timestamp');

// Environment Variables
const projectId = process.env.GOOGLE_PROJECT_ID;
const topicName = process.env.GOOGLE_TOPIC_NAME;

app.get('/', function (req, res) {
  console.log('Get request received on /');
  res.send('Browse to /publish to send a messages to Pub/Sub');
});

app.get('/test', function (req, res) {
    const number1 = Math.floor(Math.random() * Math.floor(1000));
    const number2 = Math.floor(Math.random() * Math.floor(1000));
    const number3 = Math.floor(Math.random() * Math.floor(1000));
    const data = JSON.stringify({ first: number1, second: number2, third: number3 });
    res.send(`Message published --> ${data}`);
  });

app.get('/publish', function (req, res) {
    console.log('Publish request received');

    // Create Data
    console.log('Initializing data');
    const number1 = Math.floor(Math.random() * Math.floor(1000));
    const number2 = Math.floor(Math.random() * Math.floor(1000));
    const number3 = Math.floor(Math.random() * Math.floor(1000));
    const data = JSON.stringify({ first: number1, second: number2, third: number3 });
    console.log("Data created: " + data );

    // Imports the Google Cloud client library
    const {PubSub} = require('@google-cloud/pubsub');
    
    // Instantiates a client
    const pubSubClient = new PubSub({projectId});

    // Publish message
    async function publishMessage() {
        console.log("Publishing message");

        // Publishes the message as a string, e.g. "Hello, world!" or JSON.stringify(someObject)
        const dataBuffer = Buffer.from(data);
        
        const messageId = await pubSubClient.topic(topicName).publish(dataBuffer);
        console.log(`Message ${messageId} published.`);
        res.send(`Message [Id:${messageId}] published [Data:${data}]`);
    }

    publishMessage().catch(console.error);

  });

app.listen(3000, function () {
  console.log('App listening on port 3000!');
});