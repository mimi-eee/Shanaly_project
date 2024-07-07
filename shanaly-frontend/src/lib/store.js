import { writable } from "svelte/store"

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe(
        (val) => {
            localStorage.setItem(key, JSON.stringify(val))
        }
    )
    return store
}

export const post_list_stored = persist_storage("post_list_stored", 0);

export const update_date_wiki = persist_storage("update_date_wiki", 0);
export const wiki_autocomplete_list = persist_storage("wiki_autocomplete_list", []);

export const update_date_symbol = persist_storage("update_date_symbol", 0);
export const symbol_autocomplete_list = persist_storage("symbol_autocomplete_list", []);

export const last_selected_tab = persist_storage("last_selected_tab", "");

// Account Authentication
export const access_token = persist_storage("access_token", "")
export const userid = persist_storage("userid", 0)
export const username = persist_storage("username", "")
export const email = persist_storage("email", "")
export const is_login = persist_storage("is_login", false)