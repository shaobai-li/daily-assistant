pub struct RootAgent;

impl RootAgent {
    pub fn new() -> Self {
        RootAgent
    }

    pub fn hello(&self) -> String {
        "root agent ok".to_string()
    }
}