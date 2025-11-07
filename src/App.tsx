
import ChatInput from "./components/ChatInput";
import UserMessage from "./components/UserMessage";
import AIMessage from "./components/AIMessage";
import { useState } from "react";
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
    setMessages((prev) => [...prev, {role: "user", content: message}]);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        body: JSON.stringify({content: message}),
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) throw new Error("服务器返回错误状态: ${response.status}");
      if (!response.body) throw new Error("服务器未返回流数据");
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n");
        buffer = parts.pop() ?? "";

        for (const jsonStr of parts) {
          if (!jsonStr.trim()) continue;
          try {
            const data = JSON.parse(jsonStr);
            setMessages((prev) => [...prev, {role: "assistant", content: data.message}]);

          } catch (error) {
            console.error("错误：解析 JSON:", error);
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [...prev, {role: "assistant", content: "⚠️ 无法连接到服务器，请稍后重试。"}]);
    }


  }

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
