import ChatInput from "./components/ChatInput";
import UserMessage from "./components/UserMessage";
import AIMessage from "./components/AIMessage";
import { useState } from "react";
//import "./border.css";



function App() {
  const [messages, setMessages] = useState([
    {
      role: "user",
      content: "Hello, how are you?"
    },
    {
      role: "user", 
      content: "fatal: The current branch main has no upstream branch.\nTo push the current branch and set the remote as upstream, use\n\n    git push --set-upstream origin main\n\nTo have this happen automatically for branches without a tracking\nupstream, see 'push.autoSetupRemote' in 'git help config'.\n\n什么意思怎么办"
    },
    {
      role: "assistant",
      content: "This is an AI reply."
    }
  ]);
  
  const handleSendMessage = (message) => {
    setMessages([...messages, {role: "user", content: message}]);
    console.log(messages);
  }

  return (
    <>
      <div className="chat-container"
      style={{display: "flex", flexDirection: "column", maxWidth: "840px"}}>
        {messages.map((message) => (
          message.role === "user" ? (<UserMessage message={message.content} />) : (<AIMessage message={message.content} />
          )
        ))}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </>
  )
}

export default App
