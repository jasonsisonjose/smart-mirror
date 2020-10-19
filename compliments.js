/* Magic Mirror
 * Module: Compliments
 *
 * Modified By Jason Jose
 *
 */
Module.register("compliments", {
	// Module config defaults.
	// @params: int(how often to check web-server), int (the speed of text appearing on screen)
	defaults: {
		updateInterval: 2000,
		fadeSpeed: 2000,
	},
	// Define required scripts.
	getScripts: function () {
		return ["moment.js"];
	},

	// Define start sequence.
	start: function () {
		Log.info("Starting module: " + this.name);

		this.url = "http://127.0.0.1:3000/message"
		Log.info("declaring default variables")
		this.message = "loading"
		this.timeOutMessage = ""
		this.timeOutStatus = false;
		this.lastCalled = moment()
		var self = this;

		// Schedule update timer.
		this.scheduleUpdate();
	},

	// Every update interval, it will try to get a message from the local web-server
	scheduleUpdate: function() {
		setInterval(() => {
			this.getMessage();
		}, this.config.updateInterval);
		this.getMessage();
		var self = this;
	},

	// Override dom generator.
	getDom: function () {
		var wrapper = document.createElement("div");
		wrapper.className = this.config.classes ? this.config.classes : "thin xlarge bright pre-line";
		if (this.message == "loading") {
			wrapper.innerHTML = "Loading...";
		}
		else {
			wrapper.innerHTML = this.message
		}
		if (this.timeOutStatus == true) {
			wrapper.innerHTML = this.timeOutMessage
		}
		return wrapper;
	},

	// Override notification handler.
	socketNotificationReceived: function (notification, payload) {
		// Received the data back from web-server
		console.log("received from api: ", notification);
		console.log(moment().diff(this.lastCalled, 'seconds'))
		if (notification === "MESSAGE_RESULT") {
			console.log("once attribute", payload);
			if (this.message != payload) {
				this.message = payload
				this.lastCalled = moment()
				this.updateDom(this.config.fadeSpeed)
			}
		}
		if (moment().diff(this.lastCalled, 'seconds') > 10) {
			this.message = ""
			this.timeOutStatus = true
			this.updateDom(this.config.fadeSpeed)
		}
		else {
			this.timeOutStatus = false
		}
	},

	// Notifies the socket: "HEY! check the web-server for messages!"
	getMessage: function() {
		this.sendSocketNotification('GET_MESSAGE', this.url)
	}
});
