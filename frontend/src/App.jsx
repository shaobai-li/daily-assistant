import ChatInput from "./components/ChatInput";
import UserMessage from "./components/UserMessage";
import AIMessage from "./components/AIMessage";
//import "./border.css";

function App() {
  return (
    <>
      <div className="chat-container"
      style={{display: "flex", flexDirection: "column", maxWidth: "840px"}}>
        <UserMessage message="Hello, how are you?" />
        <UserMessage message="fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

什么意思怎么办" />
        <AIMessage message="This is an AI reply." />
      </div>
      <ChatInput />
    </>
  )
}

export default App
