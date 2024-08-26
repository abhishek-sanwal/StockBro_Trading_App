// Strict mode on[ No undeclared variables allowed]
"use strict";

// Should be imported from Configurations/ Environments
const className = "room-name";
const ChannelName = "stock";
// Attributes that can change of stock data. That we need to update
const changableEntites = [
  "lastPrice",
  "prevClose",
  "lowerCircuit",
  "upperCircuit",
];

// Parse float number upto x decimals
const upto2Decimals = (num) => {
  return parseFloat(num, 2);
};

// A function to update attributes of stock data
const updateData = (event) => {
  // Parse the data from Json to Js object
  const data = JSON.parse(event.data);
  for (let element in data) {
    element = data[element];
    // For all entities other than percentage change
    for (let entity in changableEntites) {
      document.querySelector(`#a${element["symbol"]}_${entity}`).textContent =
        upto2Decimals(element[entity]);
    }
    // Seperate logic for change in percentage
    document.querySelector(`#a${element["symbol"]}_percentChange`).textContent =
      upto2Decimals(
        ((element.lastPrice - element.prevClose) * 100) / element.lastPrice
      );
  }
};

// Function to Create Socket Connection
const createSocketConnection = () => {
  // Fetch Roomname passed as context from backend
  const roomName = JSON.parse(
    document.querySelector(`#${className}`).textContent
  );
  // Search for queryString i.e. StockNames
  let queryString = window.location.search;
  queryString = queryString.substring(1);
  // console.log(queryString);

  //   Establish a websocket connection
  const stockSocket = new WebSocket(
    "ws://" +
      window.location.host +
      `/ws/${ChannelName}/` +
      roomName +
      "/" +
      "?" +
      queryString
  );

  // Display and update the data as soon as we receives messages
  stockSocket.onmessage = updateData(e);
};

const listener = document.addEventListener(
  "DOMContentLoaded",
  createSocketConnection
);
