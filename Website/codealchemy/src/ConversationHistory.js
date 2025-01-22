import React from "react";

function ConversationHistory({ messages }) {
  return (
    <div className="conversation-history">
      {messages.map((message, index) => (
        <div key={index} className={message.type === "user" ? "user-message" : message.type === "code" ? "code-message" : "chatbot-message"}>
          {message.text}
        </div>
      ))}
    </div>
  );
}

export default ConversationHistory;

