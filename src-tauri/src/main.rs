#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod command;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![command::chat_reply])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}