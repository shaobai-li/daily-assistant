import "./UserMessage.css"

interface UserMessageProps {
    message: string;
}

export default function UserMessage({message}: UserMessageProps) {
    return (
        <div className="user-message">
            <div className="user-message-bubble">
                {message}
            </div>
        </div>
    )
}