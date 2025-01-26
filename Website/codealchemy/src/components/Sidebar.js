import React from "react";
import "./Sidebar.css";

function Sidebar({ chats, activeChat, setActiveChat, onNewChat, onDeleteChat }) {
  return (
    <div className="sidebar w-72 bg-gray-800 text-white p-6 overflow-y-auto">
      <div className="sidebar-header mb-6 flex justify-between items-center">
        <h2 className="text-lg font-medium">Chat History</h2>
        <button
          onClick={onNewChat}
          className="new-chat-button bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
        >
          + New Chat
        </button>
      </div>
      <ul>
        {chats.map((chat) => (
          <li
            key={chat.id}
            className={`px-4 py-3 mb-2 bg-gray-700 rounded-md cursor-pointer flex justify-between items-center ${
              chat.id === activeChat?.id ? "bg-gray-600" : "hover:bg-gray-600"
            }`}
            onClick={() => setActiveChat(chat)}
          >
            {chat.name || "Untitled Chat"}
            <button
              className="delete-button text-white hover:text-red-500"
              onClick={(e) => {
                e.stopPropagation();
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