import React, { useState } from "react";
import "./TextInput.css";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";

function TextInput({ onSend }) {
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const { transcript, resetTranscript } = useSpeechRecognition();

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }
    // Call onSend with the file
    onSend(null, file);
    setFile(null); // Clear the file input after the upload
  };

  // Handle sending a chat message
  const handleSend = async () => {
    if (input.trim() === "") return;
    onSend(input, null); // Call onSend with the input message
    setInput(""); // Clear the input field
  };

  const toggleListening = () => {
    if (!isListening) {
      SpeechRecognition.startListening({ continuous: true });
    } else {
      SpeechRecognition.stopListening();
      setInput(transcript); // Set the transcript in the input field
      resetTranscript(); // Clear the transcript after using it
    }
    setIsListening(!isListening);
  };

  return (
    <div className="text-input-container">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={handleSend}>Send</button>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <button
        className="mic-button"
        onClick={toggleListening}
        style={{ backgroundColor: isListening ? "#000000" : "#007bff" }}
      >
        🎙️
      </button>
    </div>
  );
}

export default TextInput;
