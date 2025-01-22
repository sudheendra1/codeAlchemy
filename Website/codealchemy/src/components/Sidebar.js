import React from "react";
import "./Sidebar.css";

function Sidebar({ chats, activeChat, setActiveChat, onNewChat, onDeleteChat }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Chat History</h2>
        <button onClick={onNewChat} className="new-chat-button">
          + New Chat
        </button>
      </div>
      <ul>
        {chats.map((chat) => (
          <li
            key={chat.id}
            className={chat.id === activeChat?.id ? "active" : ""}
            onClick={() => setActiveChat(chat)}
          >
            {chat.name || "Untitled Chat"}
            <button
              className="delete-button"
              onClick={(e) => {
                e.stopPropagation(); // Prevent selecting the chat
                onDeleteChat(chat.id);
              }}
            >
              🗑️
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;
