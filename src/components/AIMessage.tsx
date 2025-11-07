import "./AIMessage.css"
import ReactMarkdown from "react-markdown"

interface AIMessageProps {
    message: string;
}

export default function AIMessage({message}: AIMessageProps) {
    return (
        <div className="ai-message">
            <div className="ai-message-bubble">
                <ReactMarkdown>{message}</ReactMarkdown>
            </div>
        </div>
    )
}