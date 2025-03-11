export function makeParamsString(params) {
    if (!(typeof params === "object")) {
        throw TypeError("Params object must be an object");
    }

    const paramsArray = [];
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            paramsArray.push(`${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`);
        }
    }
    return paramsArray.join('&');
}