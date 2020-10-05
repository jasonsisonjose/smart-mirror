const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
const port = 3000;

let previousMessage={};
let updatedMessage={};

// if a message is the same as a previous message, then send the same previous message
// else: send the new updated message
app.get('/message', (req,res) => {
  if (previousMessage === updatedMessage) {
    res.send(previousMessage);
  }
  else {
    previousMessage = updatedMessage
    res.send(previousMessage);
  }
})

// Post for changing the default message
// Expecting this format: "{'Message': '<message-contents'}"
app.post('/message', (req, res) => {
  updatedMessage = req.body;
  console.log(req.body);
  res.send("we are done changing the default message");
})

app.listen(port, () => {
  console.log('listening on http://localhost:', port);
})
