import React, { useState } from "react"
import "./TextInput.css"
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition"
import { Mic, Send, Upload } from "lucide-react"

function TextInput({ onSend }) {
  const [input, setInput] = useState("")
  const [file, setFile] = useState(null)
  const [isListening, setIsListening] = useState(false)
  const { transcript, resetTranscript } = useSpeechRecognition()

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.")
      return
    }
    onSend(null, file)
    setFile(null)
  }

  const handleSend = async () => {
    if (input.trim() === "") return
    onSend(input, null)
    setInput("")
  }

  const toggleListening = () => {
    if (!isListening) {
      SpeechRecognition.startListening({ continuous: true })
    } else {
      SpeechRecognition.stopListening()
      setInput(transcript)
      resetTranscript()
    }
    setIsListening(!isListening)
  }

  return (
    <div className="text-input-container">
      <textarea value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type your message..." />
      <button className="send-button" onClick={handleSend}>
        <Send size={18} />
      </button>
      <input type="file" onChange={handleFileChange} style={{ display: "none" }} id="file-input" />
      <label htmlFor="file-input">
        <button className="upload-button" onClick={() => document.getElementById("file-input").click()}>
          Choose File
        </button>
      </label>
      {file && (
        <button className="upload-button" onClick={handleUpload}>
          <Upload size={18} />
        </button>
      )}
      <button className={`mic-button ${isListening ? "active" : ""}`} onClick={toggleListening}>
        <Mic size={18} />
      </button>
    </div>
  )
}

export default TextInput

