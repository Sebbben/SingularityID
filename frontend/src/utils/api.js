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
     * @returns {Promise<Object>} - The JSON response from the server.
     */
    static async GET(url, args = null, options = {}) {
        let endpoint = args ? url + "?" + makeParamsString(args) : url;
        let res = await fetch(endpoint, options)
        .then(this.extractJSONResponse)
        
        return res
    }

    /**
     * Makes a POST request to the specified URL with the given arguments.
     * @param {string} url - The URL to make the POST request to.
     * @param {Object} args - The arguments to include in the request body.
     * @param {Object} [options={}] - Additional fetch options.
     * @returns {Promise<Object>} - The JSON response from the server.
     */
    static async POST(url, args, options = {}) {
        let res = await fetch(url, {
            method: "POST",
            body: JSON.stringify(args),
            headers: {
                "Content-Type": "application/json",
                ...options.headers // Merge headers correctly
            },
            ...options
        })
        .then(this.extractJSONResponse)

        
        return res
    }

    static async extractJSONResponse(res) {
        if (!(200 <= res.status <= 399)) return [res.status, null]
        try {
            let json = await res.json()
            if (300 <= res.status <= 399 && json.redirect_uri) API.handleRedirect(json.redirect_uri)
            return [res.status, json];
        } catch (err) {
            if (err instanceof SyntaxError) {
                console.warn("Could not read json of api response");
                console.warn(res);
            } else {
                throw err; // Re-throw other errors
            }
            return [res.status, null]
        }
    }

    static async handleRedirect(url) {
        if (typeof window !== "undefined") { // Client component
            window.location = url
        } else { // Server component // TODO : Possibly implement url validation to prevent redirection to mallisious urls
            redirect(url);
        }
    }
}

export default API;