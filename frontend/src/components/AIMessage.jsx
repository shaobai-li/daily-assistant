import "./AIMessage.css"

export default function AIMessage({message}) {
    return (
        <div className="ai-message">
            <div className="ai-message-bubble">
                {message}
            </div>
        </div>
    )
}