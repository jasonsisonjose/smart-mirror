const NodeHelper = require("node_helper");
const request = require("request");

module.exports = NodeHelper.create({
	start: function() {
		console.log("Starting node_helper for: " + this.name);
	},
	socketNotificationReceived: function(notification, payload) {
		console.log("notification received: ", notification)
		switch(notification) {
			case "GET_MESSAGE":
				console.log("running get_message notification")
				this.getMessage(payload);
		}
	},
	// Calls the web-server to get the message
	getMessage: function(url) {
		console.log("web server url: ", url);
		request({
			url: "http://localhost:3000/message",
			method: 'GET'
		}, (error, response, body) => {
			//console.log("error: ", error);
			//console.log("response: ", response);
			//console.log("body: ", body);
			if (!error && response.statusCode == 200) {
				bodyJson = JSON.parse(body)
				console.log("this is my body: ", bodyJson['Message'])
				this.sendSocketNotification('MESSAGE_RESULT', bodyJson['Message'])
			}
		});
	}
});
