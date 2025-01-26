import React, { useState } from "react";
import "./TextInput.css";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";

function TextInput({ onSend }) {
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const { transcript, resetTranscript } = useSpeechRecognition();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }
    onSend(null, file);
    setFile(null);
  };

  const handleSend = async () => {
    if (input.trim() === "") return;
    onSend(input, null);
    setInput("");
  };

  const toggleListening = () => {
    if (!isListening) {
      SpeechRecognition.startListening({ continuous: true });
    } else {
      SpeechRecognition.stopListening();
      setInput(transcript);
      resetTranscript();
    }
    setIsListening(!isListening);
  };

  return (
    <div className="text-input-container bg-white p-4 flex items-center shadow-md">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="flex-grow resize-none px-4 py-2 border border-gray-300 rounded-md"
        placeholder="Type your message..."
      />
      <button
        onClick={handleSend}
        className="ml-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
      >
        Send
      </button>
      <input
        type="file"
        onChange={handleFileChange}
        className="ml-4"
      />
      <button
        onClick={handleUpload}
        className="ml-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
      >
        Upload
      </button>
      <button
        className={`ml-4 p-2 rounded-full ${
          isListening ? "bg-black text-white" : "bg-blue-500 hover:bg-blue-600 text-white"
        }`}
        onClick={toggleListening}
      >
        🎙️
      </button>
    </div>
  );
}

export default TextInput;