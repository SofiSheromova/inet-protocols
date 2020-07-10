const {buildUrl, promiseRequest} = require('./helpers')
const config = require('config')

function authorize(req, res) {
    res.redirect(getAuthorizeRequestString())
}

let token = {
    accessToken: '',
    userId: '',
};

function createToken(req, res) {
    getAccessToken(req.query.code)
        .then(data => {
            token.accessToken = data.access_token
        })
        .then(() => res.redirect('/form'))
        .catch(() => {
            res.send('Произошла ошибка доступа. Попробуйте повторить попытку позже.')
        })
}

function getAccessToken(vkCode) {
    return promiseRequest(getAccessTokenRequestString(vkCode), true)
}

function getAuthorizeRequestString() {
    const options = {
        client_id: '7441874',
        redirect_uri: 'http://localhost:3000/code/',
        scope: 'friends',
        response_type: 'code',
        v: '5.103'
    }
    return buildUrl('https://oauth.vk.com/authorize', options)
}

function getAccessTokenRequestString(code) {
    const options = {
        client_id: '7441874',
        client_secret: 'ROMeVHRu7d2AFbWaWmqo',
        redirect_uri: `http://localhost:${config.get('port')}/code/`,
        code: code
    }

    return buildUrl('https://oauth.vk.com/access_token', options)
}

module.exports = {
    authorize,
    createToken,
    token
}
