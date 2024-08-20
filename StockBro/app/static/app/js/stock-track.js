// Javascript

console.log(" Javascript is attached and running as well.");
document.addEventListener("DOMContentLoaded", () => {
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
    // console.log(data, "Our data is this.");
    for (element in data) {
      element = data[element];
      document.querySelector(`#a${element["symbol"]}_lastPrice`).textContent =
        element.lastPrice;
      document.querySelector(`#a${element["symbol"]}_prevClose`).textContent =
        element.prevClose;
      document.querySelector(
        `#a${element["symbol"]}_percentChange`
      ).textContent = element.lastPrice - element.prevClose;
      document.querySelector(
        `#a${element["symbol"]}_lowerCircuit`
      ).textContent = element.lowerCircuit;
      document.querySelector(
        `#a${element["symbol"]}_upperCircuit`
      ).textContent = element.upperCircuit;
    }
  };
});
