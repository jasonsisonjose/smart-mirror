const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
const port = 3000;

let previousMessage={};
let updatedMessage={};

app.get('/message', (req,res) => {
  if (previousMessage === updatedMessage) {
    res.send(previousMessage);
  }
  else {
    previousMessage = updatedMessage
    res.send(previousMessage);
  }
})

app.post('/message', (req, res) => {
  updatedMessage = req.body;
  console.log(req.body);
  res.send("we are done changing the default message");
})

app.listen(port, () => {
  console.log('listening on http://localhost:', port);
})
