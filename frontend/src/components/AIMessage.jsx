import "./AIMessage.css"

export default function AIMessage({message}) {
    return (
        <div className="ai-message">
            <div className="ai-message-bubble">
                <text>{message}</text>
            </div>
        </div>
    )
}