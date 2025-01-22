function CombinedComponent() {
    const [data, setData] = useState(null);
  
    const fetchData = () => {
      axios
        .get("https://example.com/api/data")
        .then((response) => setData(response.data))
        .catch((error) => console.error("Error fetching data:", error));
    };
  
    const sendData = () => {
      axios
        .post("https://example.com/api/data", { name: "Jane Doe" })
        .then((response) => {
          console.log("Data sent successfully:", response.data);
          fetchData(); // Fetch updated data after sending
        })
        .catch((error) => console.error("Error sending data:", error));
    };
  
    useEffect(() => {
      fetchData();
    }, []);
  
    return (
      <div>
        <button onClick={sendData}>Send Data</button>
        <h1>Fetched Data:</h1>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  }
  
  export default CombinedComponent;
  