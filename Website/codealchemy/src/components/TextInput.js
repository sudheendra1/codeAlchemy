import React, { useState } from "react";
import "./TextInput.css";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";

function TextInput({ onSend }) {
  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const { transcript, resetTranscript } = useSpeechRecognition();

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput(""); // Clear input after sending
    }
  };

  const toggleListening = () => {
    setIsListening(!isListening); // Toggle the listening state
    if (!isListening) {
        SpeechRecognition.startListening({ continuous: true });
      } else {
        SpeechRecognition.stopListening();
        setInput(transcript); // Set the transcript in the text input
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
      <button className="mic-button" onClick={toggleListening} style={{ backgroundColor: isListening ? "#000000" : "#007bff" }}>
      🎙️
      </button>
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default TextInput;
