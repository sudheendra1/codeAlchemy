import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import TextInput from "./components/TextInput";
import "./App.css";

function App() {
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);

  const handleSendMessage = (message) => {
    if (!activeChat) return;

    setChats((prevChats) =>
      prevChats.map((chat) =>
        chat.id === activeChat.id
          ? {
              ...chat,
              messages: [...chat.messages, { text: message, type: "user" }],
              name: chat.messages.length === 0 ? message : chat.name,
            }
          : chat
      )
    );

    // Update the active chat to trigger re-render
    setActiveChat((prevChat) => ({
      ...prevChat,
      messages: [...prevChat.messages, { text: message, type: "user" }],
    }));
  };

  const handleNewChat = () => {
    const newChat = {
      id: Date.now(),
      name: "New Chat",
      messages: [],
    };
    setChats([newChat, ...chats]);
    setActiveChat(newChat);
  };

  const handleDeleteChat = (id) => {
    setChats(chats.filter((chat) => chat.id !== id));
    if (activeChat?.id === id) setActiveChat(null);
  };

  return (
    <div className="app">
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        setActiveChat={setActiveChat}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
      />
      <div className="main">
        {activeChat ? (
          <>
            <ChatArea messages={activeChat.messages} />
            <TextInput onSend={handleSendMessage} />
          </>
        ) : (
          <div className="no-chat-selected">
            <h2>Select a chat or start a new one</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
