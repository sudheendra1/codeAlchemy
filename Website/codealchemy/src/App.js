import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import TextInput from "./components/TextInput";
import axios from "axios";
import "./App.css";

function App() {
  var count = 0;
  var textCount =0;
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);

  const handleSendMessage = async (message, file) => {
    if (!activeChat) return;

    if (file) {
      const documentName = file.name;

      setChats((prevChats) =>
        prevChats.map((chat) =>
          chat.id === activeChat.id
            ? {
                ...chat,
                messages: [
                  ...chat.messages,
                  { text: `Uploading file: ${documentName}`, type: "user" },
                ],
              }
            : chat
        )
      );

      setActiveChat((prevChat) => ({
        ...prevChat,
        messages: [
          ...prevChat.messages,
          { text: `Uploading file: ${documentName}`, type: "user" },
        ],
      }));

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        const { message: uploadMessage, llm_processed_json } = response.data;
        const generatedText = llm_processed_json.results[0].generated_text; 
        count++;

        setChats((prevChats) =>
          prevChats.map((chat) =>
            chat.id === activeChat.id
              ? {
                  ...chat,
                  messages: [
                    ...chat.messages,
                    { text: `File uploaded: ${uploadMessage}`, type: "system" },
                    { text: generatedText, type: "chatbot" },
                    {text: "Please provide the query you want resolved",type:"chatbot"},
                  ],
                }
              : chat
          )
        )

        setActiveChat((prevChat) => ({
          ...prevChat,
          messages: [
            ...prevChat.messages,
            { text: `File uploaded: ${uploadMessage}`, type: "system" },
            { text: generatedText, type: "chatbot" },
            count===1?{text: "Please provide the query you want resolved",type:"chatbot"}:{text: "",type:"chatbot"},
          ],
        }));
      } catch (error) {
        console.error("Error uploading file:", error);
        setChats((prevChats) =>
          prevChats.map((chat) =>
            chat.id === activeChat.id
              ? {
                  ...chat,
                  messages: [
                    ...chat.messages,
                    { text: "Error uploading file. Please try again.", type: "system" },
                  ],
                }
              : chat
          )
        );
      }
    } else {
      if(textCount==0){
        setChats((prevChats) =>
          prevChats.map((chat) =>
            chat.id === activeChat.id
              ? {
                  ...chat,
                  messages: [
                    ...chat.messages,
                    { text: message, type: "user" },
                    { text: "please provide the stacktrace of your error", type: "chatbot" },
                  ],
                  name: chat.messages.length === 0 ? message : chat.name,
                }
              : chat
          )
        );

        setActiveChat((prevChat) => ({
          ...prevChat,
          messages: [
            ...prevChat.messages,
            { text: message, type: "user" },
            { text: "please provide the stacktrace of your error", type: "chatbot" },
          ],
        }));

      }
      else{
      try {
        const response = await axios.post("http://127.0.0.1:5000/chat", { message });
        const { response: assistantResponse } = response.data;

        setChats((prevChats) =>
          prevChats.map((chat) =>
            chat.id === activeChat.id
              ? {
                  ...chat,
                  messages: [
                    ...chat.messages,
                    { text: assistantResponse, type: "chatbot" },
                  ],
                  name: chat.messages.length === 0 ? message : chat.name,
                }
              : chat
          )
        );

        setActiveChat((prevChat) => ({
          ...prevChat,
          messages: [
            ...prevChat.messages,
            { text: assistantResponse, type: "chatbot" },
          ],
        }));
      } catch (error) {
        console.error("Error sending message:", error);
        setChats((prevChats) =>
          prevChats.map((chat) =>
            chat.id === activeChat.id
              ? {
                  ...chat,
                  messages: [
                    ...chat.messages,
                    { text: "Error: Unable to get a response from the chatbot.", type: "system" },
                  ],
                }
              : chat
          )
        );
      }}
    }
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
    <div className="app bg-gray-100 flex h-screen">
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        setActiveChat={setActiveChat}
        onNewChat={handleNewChat}
        onDeleteChat={handleDeleteChat}
      />
      <div className="main flex-grow">
        {activeChat ? (
          <>
            <ChatArea messages={activeChat.messages} />
            <TextInput onSend={handleSendMessage} />
          </>
        ) : (
          <div className="no-chat-selected flex items-center justify-center h-full">
            <h2 className="text-gray-500 text-xl">Select a chat or start a new one</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;