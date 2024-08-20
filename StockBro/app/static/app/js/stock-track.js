// Javascript

console.log(" Javascript is attached and running as well.");
document.addEventListener("DOMContentLoaded", () => {
  const roomName = JSON.parse(document.getElementById("room-name").textContent);
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
  // console.log(stockSocket + " Web socket is created");
  // Display and update the data as soon as we receives messages
  stockSocket.onmessage = function (e) {
    console.log(e.data);
    const data = JSON.parse(e.data);
    console.log(data);
  };
});
