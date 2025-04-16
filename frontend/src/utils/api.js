import { makeParamsString } from "./general"
import { redirect } from "next/navigation"

/**
 * Static API class to handle GET and POST requests.
 */
class API {
    /**
     * Makes a GET request to the specified URL with the given arguments.
     * @param {string} url - The URL to make the GET request to.
     * @param {Object} args - The arguments to include in the query string.
     * @param {Object} [options={}] - Additional fetch options.
     * @param {Function} [success=()=>{}] - Callback function to handle successful response.
     * @param {Function} [error=()=>{}] - Callback function to handle error response.
     * @returns {Promise<Object>} - The JSON response from the server.
     */
    static async GET(url, args = null, options = {}, success = ()=>{}, error = ()=>{}) {
        let endpoint = args ? url + "?" + makeParamsString(args) : url;
        let json = await fetch(endpoint, options)
        .then(async res => {
            if (res.ok) {
                try {
                    let json = await res.json()
                    success(json)
                    return json
                } catch {
                    console.warn("Could not read json of api response");
                    console.warn(res);
                }
            } else if ( 300 <= res.status <= 399) {
                try {
                    let json = await res.json()
                    if (json.redirect_uri) {
                        redirect(json.redirect_uri)
                    } else {
                        console.log(json)
                    }
                    return json
                } catch (err) {
                    if (err instanceof SyntaxError) {
                        console.warn("Could not read json of api response");
                        console.warn(res);
                    } else {
                        throw err; // Re-throw other errors
                    }
                    console.warn("Could not read json of api response");
                    console.warn(res);
                }
            } else {
                error(res.status, res.error)
                return {res}
            }
        })
        
        return json
    }

    /**
     * Makes a POST request to the specified URL with the given arguments.
     * @param {string} url - The URL to make the POST request to.
     * @param {Object} args - The arguments to include in the request body.
     * @param {Object} [options={}] - Additional fetch options.
     * @param {Function} [success=()=>{}] - Callback function to handle successful response.
     * @param {Function} [error=()=>{}] - Callback function to handle error response.
     * @returns {Promise<Object>} - The JSON response from the server.
     */
    static async POST(url, args, options = {}, success = ()=>{}, error = ()=>{}) {
        let json = await fetch(url, {
            method: "POST",
            body: JSON.stringify(args),
            headers: {
                "Content-Type": "application/json",
                ...options.headers // Merge headers correctly
            },
            ...options
        })
        .then(async res => {
            if (res.ok) {
                let json = await res.json()
                success(json)
    
                return json
            } else if ( 300 <= res.status <= 399) {
                let json = await res.json()
                if (json.redirect_uri) {
                    redirect(json.redirect_uri)
                } else {
                    console.log(json)
                }
                return json

            } else {
                error(res.status, res.error)
                return {res}
            }
        })
        
        return json
    }
}

export default API;