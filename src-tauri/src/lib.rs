// src-tauri/src/lib.rs

use log::LevelFilter;

// 定义一个可以被前端调用的命令
#[tauri::command]
fn chat_reply(content: String) -> String {
    println!("收到前端消息: {}", content);
    format!("这是来自 Rust 的回复：{}", content)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // 注册前端可以调用的命令
        .invoke_handler(tauri::generate_handler![chat_reply])
        // setup 是应用初始化时执行的逻辑
        .setup(|app| {
            // 如果是开发模式（debug）
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        // 启动应用
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
