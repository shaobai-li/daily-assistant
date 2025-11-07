import "./AIMessage.css"
import ReactMarkdown from "react-markdown"

export default function AIMessage({message}) {
    return (
        <div className="ai-message">
            <div className="ai-message-bubble">
                <ReactMarkdown>{message}</ReactMarkdown>
            </div>
        </div>
    )
}