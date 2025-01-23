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
          <p>Before I can provide you the solution to your problem please give me a little a context by giving me the README file(recommended) for your project or a detailed text input.</p>
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
