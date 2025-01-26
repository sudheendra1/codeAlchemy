import React from "react"
import "./Sidebar.css"
import { Trash2, Plus } from "lucide-react"

function Sidebar({ chats, activeChat, setActiveChat, onNewChat, onDeleteChat }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Chat History</h2>
        <button onClick={onNewChat} className="new-chat-button">
          <Plus size={16} />
          <span>New Chat</span>
        </button>
      </div>
      <ul>
        {chats.map((chat) => (
          <li key={chat.id} className={chat.id === activeChat?.id ? "active" : ""} onClick={() => setActiveChat(chat)}>
            <span className="chat-name">{chat.name || "Untitled Chat"}</span>
            <button
              className="delete-button"
              onClick={(e) => {
                e.stopPropagation()
                onDeleteChat(chat.id)
              }}
            >
              <Trash2 size={16} />
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Sidebar

