use crate::agents::root_agent::RootAgent;

#[tauri::command]
pub async fn chat_reply(content: String) -> Result<String, String> {
    println!("收到前端消息: {}", content);

    use dotenvy::dotenv;
    use std::env;
    use reqwest::Client;
    use serde_json::json;

    dotenv().ok();
    let api_key = env::var("DEEPSEEK_API_KEY").map_err(|e| e.to_string())?;
    let client = Client::new();
    let url = "https://api.deepseek.com/v1/chat/completions";
    let body = json!({
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": content}
        ]
    });

    let resp = client
        .post(url)
        .bearer_auth(&api_key)
        .json(&body)
        .send()
        .await
        .map_err(|e| e.to_string())?;

    let text = resp.text().await.map_err(|e| e.to_string())?;
    Ok(text)
}

#[tauri::command]
pub fn agent_ping() -> Result<String, String> {

    let agent = RootAgent::new()?;
    Ok(agent.hello())
}