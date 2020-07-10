const request = require('request');

function promiseRequest(url, detectError = false) {
    return new Promise((resolve, reject) => {
        request(url, (err, res, body) => {
            if (err) {
                reject(err);
            } else {
                const data = JSON.parse(body);
                if (detectError && data.hasOwnProperty('error')) {
                    reject(data.error)
                } else {
                    resolve(data);
                }
            }
        })
    })
}

function buildUrl(address, params) {
    const queryString = new URLSearchParams();
    for (let key in params) {
        if (!params.hasOwnProperty(key)) {
            continue;
        }
        queryString.set(key, params[key])
    }

    return address + '?' + queryString.toString();
}

module.exports = {
    promiseRequest,
    buildUrl
}
