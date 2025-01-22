function DataSendingComponent() {
    const sendData = () => {
      axios
        .post("https://example.com/api/data", {
          name: "John Doe",
          age: 30,
        })
        .then((response) => {
          console.log("Data sent successfully:", response.data);
        })
        .catch((error) => {
          console.error("Error sending data:", error);
        });
    };
  
    return <button onClick={sendData}>Send Data</button>;
  }
  
  export default DataSendingComponent;
  