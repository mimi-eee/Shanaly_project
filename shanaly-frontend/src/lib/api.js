import qs from 'qs';
import { push } from 'svelte-spa-router';
import { get } from 'svelte/store';
import { access_token, userid, username, email, is_login } from './store';
const base_url = import.meta.env.VITE_BACKEND_SERVER_URL;

async function fastapi(operation, end_point, params={}, success_callback, failure_callback) {

    // Example of query params:
    // let params = {
    //     symbol: "6920.T",
    //     market: "TSE"
    // }

    let method = operation.toLowerCase();
    let endpoint = end_point;
    let option = {};
    let body = JSON.stringify(params);
    
    if (method === "get") {
        
        option = {
            method: "GET",
            headers: {"Content-Type": "application/json"}
        };

        if (params !== {}) {
            endpoint += "?"
            endpoint += new URLSearchParams(params)
        }

    } else if (method === "post") {
        
        option = {
            method: "POST",
            headers: {"Content-Type": "application/json"}
        }

        if (params !== {}) {
            option["body"] = body;
        }

    } else if (method === "patch") {
        
        option = {
            method: "PATCH",
            headers: {"Content-Type": "application/json"}
        }

        if (params !== {}) {
            option["body"] = body;
        }

    } else if (method === "delete") {
        
        option = {
            method: "DELETE",
            headers: {"Content-Type": "application/json"}
        }

        if (params !== {}) {
            option["body"] = body;
        }
    
    } else if (method === 'login') {

        body = qs.stringify(params)
        option = {
            method: "POST",
            headers: {"Content-Type": 'application/x-www-form-urlencoded'}
        }

        if (params !== {}) {
            option["body"] = body;
        }
    } else {
        throw new Error('Choose acceptable operations (method) only!');
    }

    const _access_token = get(access_token)
    if (_access_token) {
        option.headers["Authorization"] = "Bearer " + _access_token
    }

    try {
        let res = await fetch(`${base_url}${endpoint}`, option);

        // Authentication: 403 (Unauthorized, Forbidden) or 401 (Token Expired)
        if (operation !== "login" && (res.status === 403 || res.status === 401)) {
            //token time out
            access_token.set("");
            userid.set(0);
            username.set("");
            email.set("");
            is_login.set(false);
            
            try {
                // Add a code for closing the opened modal and remove backdrop effect!
                document.querySelector("[id='detail-modal-button']").click();
            } catch {
                // Do nothing
            }
            
            // Return the user to login page
            push("/user-login");
            return;
        }

        if (res.status >= 200 && res.status < 300) {

            let result = await res.json();
            success_callback(result)

        } else {

            let result = await res.json();
            failure_callback(result)
        }
        
    } catch (err) {

        console.log(err);

    }
}

export default fastapi