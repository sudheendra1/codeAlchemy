import React, { useEffect, useRef } from "react";
import "./ChatArea.css";

function ChatArea({ messages }) {
  const chatEndRef = useRef(null);

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-area">
      {messages.length === 0 && (
        <div className="no-messages">
          <p>Start the conversation by typing a message.</p>
        </div>
      )}
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message ${message.type === "user" ? "user" : "chatbot"}`}
        >
          {message.text}
        </div>
      ))}
      <div ref={chatEndRef} />
    </div>
  );
}

export default ChatArea;
