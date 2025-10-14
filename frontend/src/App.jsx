import ChatInput from "./components/ChatInput";
import UserMessage from "./components/UserMessage";
import AIMessage from "./components/AIMessage";
import { useState } from "react";
//import "./border.css";



function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Good day! 白哥"
    }
  ]);
  
  const handleSendMessage = (message) => {
    setMessages([...messages, {role: "user", content: message}]);
    console.log(messages);

    fetch("/chat", {
      method: "POST",
      body: JSON.stringify({content: message}),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(response => response.json())
    .then(data => {
      setMessages([...messages, {role: "assistant", content: data.message}]);
    })
    .catch(error => {
      console.error("Error:", error);
    });
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
