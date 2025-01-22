import React from "react";

function MessageDisplay({ messages }) {
  return (
    <div className="message-display">
      {messages.map((message, index) => (
        <div key={index} className={message.type === "user" ? "user-message" : message.type === "code" ? "code-message" : "chatbot-message"}>
          {message.text}
        </div>
      ))}
    </div>
  );
}

export default MessageDisplay;
