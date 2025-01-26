import React, { useEffect, useRef } from "react";
import "./ChatArea.css";

function ChatArea({ messages }) {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-area bg-gray-100 flex-grow p-8 overflow-y-auto">
      {messages.length === 0 && (
        <div className="no-messages flex items-center justify-center h-full text-gray-500">
          <p>Before I can provide you the solution to your problem please give me a little a context by giving me the README file(recommended) for your project or a detailed text input.</p>
        </div>
      )}
      {messages.map((message, index) => (
        <div
          key={index}
          className={`message mb-4 px-6 py-4 max-w-[70%] word-break rounded-2xl text-center ${
            message.type === "user"
              ? "bg-blue-500 text-white self-end rounded-br-none"
              : "bg-gray-400 self-start rounded-bl-none"
          }`}
        >
          {message.text}
        </div>
      ))}
      <div ref={chatEndRef} />
    </div>
  );
}

export default ChatArea;