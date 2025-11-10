use std::env;

pub struct RootAgent {
    api_key: String,
}

impl RootAgent {
    pub fn new() -> Result<Self, String> {
        dotenvy::dotenv().ok();
        let api_key = env::var("DEEPSEEK_API_KEY").map_err(|e| e.to_string())?;
        Ok(Self { api_key})
    }

    pub fn hello(&self) -> String {
        format!("root agent ok, key.length: {}", self.api_key.len())
    }
}