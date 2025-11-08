#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use dotenvy::dotenv;
use std::env;
use reqwest::Client;
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    dotenv().ok();

    let api_key = env::var("DEEPSEEK_API_KEY").expect("DEEPSEEK_API_KEY not found");
    let client = Client::new();
    let url = "https://api.deepseek.com/v1/chat/completions";

    // 你的输入
    let prompt = "请用一句话解释量子纠缠";

    let body = json!({
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    });

    let resp = client
        .post(url)
        .bearer_auth(&api_key)
        .json(&body)
        .send()
        .await?;

    let text = resp.text().await?;
    println!("DeepSeek Response:\n{}", text);

    Ok(())
}
