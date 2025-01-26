import React, { useEffect, useRef } from "react"
import "./ChatArea.css"

function ChatArea({ messages }) {
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [chatEndRef]) //Fixed unnecessary dependency

  return (
    <div className="chat-area">
      {messages.length === 0 && (
        <div className="no-messages">
          <p>Start a conversation or upload a file to begin.</p>
        </div>
      )}
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.type === "user" ? "message-user" : "message-bot"}`}>
          {message.text}
        </div>
      ))}
      <div ref={chatEndRef} />
    </div>
  )
}

export default ChatArea

