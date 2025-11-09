// src-tauri/src/lib.rs

use log::LevelFilter;

// 定义一个可以被前端调用的命令
#[tauri::command]
fn fixed_chat_reply(content: String) -> String {
    println!("收到前端消息: {}", content);
    format!("这是来自 Rust 的回复：{}", content)
}

#[tauri::command]
async fn chat_reply(content: String) -> Result<String, String> {
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



#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // 注册前端可以调用的命令
        .invoke_handler(tauri::generate_handler![chat_reply])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
