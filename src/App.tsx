
import ChatInput from "./components/ChatInput";
import UserMessage from "./components/UserMessage";
import AIMessage from "./components/AIMessage";
import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
//import "./border.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Good day! 白哥"
    }
  ]);
    
  const handleSendMessage = async (message: string) => {
    setMessages((prev) => [...prev, { role: "user", content: message }]);

    try {
      const reply = await invoke<string>("chat_reply", { content: message });

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: reply },
      ]);
    } catch (error) {
      console.error("Error invoking Rust command:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ 无法连接到后端，请稍后重试。" },
      ]);
    }
  };

  return (
    <>
      <div className="chat-container"
      style={{display: "flex", flexDirection: "column", maxWidth: "840px"}}>
        {messages.map((message, index) => (
          message.role === "user" ? (<UserMessage key={index} message={message.content} />) : (<AIMessage key={index} message={message.content} />
          )
        ))}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </>
  )
}

export default App
