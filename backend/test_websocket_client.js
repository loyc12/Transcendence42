const WebSocket = require('ws');

const socket = new WebSocket('ws://localhost:3000');

socket.onopen = function () {
console.log('WebSocket connection opened.');
};

socket.onmessage = function (event) {
console.log('Received message from server:', event.data);
};

socket.onclose = function (event) {
console.log('WebSocket connection closed:', event.code, event.reason);
};