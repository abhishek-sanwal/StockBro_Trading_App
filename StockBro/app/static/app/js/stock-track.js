// Javascript

// Strict mode on[ No undeclared variables allowed]
"use strict";

// Parse float number upto x decimals
const uptoDecimals = (num, x) => {
  return parseFloat(num, x);
};

const listener = document.addEventListener("DOMContentLoaded", () => {
  // Fetech Roomname passed as context from backend
  const roomName = JSON.parse(document.querySelector("#room-name").textContent);

  // Search for queryString i.e. StockNames
  let queryString = window.location.search;
  queryString = queryString.substring(1);
  // console.log(queryString);

  //   Establish a websocket connection
  const stockSocket = new WebSocket(
    "ws://" +
      window.location.host +
      "/ws/stock/" +
      roomName +
      "/" +
      "?" +
      queryString
  );

  // Display and update the data as soon as we receives messages
  stockSocket.onmessage = function (e) {
    // console.log(e.data);
    const data = JSON.parse(e.data);
    console.log(data, "Our data is this.");
    for (let element in data) {
      element = data[element];
      document.querySelector(`#a${element["symbol"]}_lastPrice`).textContent =
        uptoDecimals(element.lastPrice, 2);
      document.querySelector(`#a${element["symbol"]}_prevClose`).textContent =
        uptoDecimals(element.prevClose, 2);
      document.querySelector(
        `#a${element["symbol"]}_percentChange`
      ).textContent = uptoDecimals(
        ((element.lastPrice - element.prevClose) * 100) / element.lastPrice,
        2
      );
      document.querySelector(
        `#a${element["symbol"]}_lowerCircuit`
      ).textContent = uptoDecimals(element.lowerCircuit, 2);
      document.querySelector(
        `#a${element["symbol"]}_upperCircuit`
      ).textContent = uptoDecimals(element.upperCircuit, 2);
    }
  };
});
