import "./UserMessage.css"

export default function UserMessage({message}) {
    return (
        <div className="user-message">
            <div className="user-message-bubble">
                {message}
            </div>
        </div>
    )
}