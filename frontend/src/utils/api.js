import { makeParamsString } from "./general"

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
    static async GET(url, args, options = {}, success = ()=>{}, error = ()=>{}) {
        let json = await fetch(url + "?" + makeParamsString(args), options)
        .then(async res => {
            if (!res.ok) {
                error(res.status, res.error)
                return {res}
            }

            let json = await res.json()
            success(json)

            return json
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
            if (!res.ok) {
                error(res.status, res.error)
                return {res}
            }

            let json = await res.json()
            success(json)

            return json
        })
        
        return json
    }
}

export default API;