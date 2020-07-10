const {promiseRequest, buildUrl} = require('./helpers')
const {token} = require('./token')

function displayForm(req, res) {
    res.render('start')
}

function requestWallPost(req, res) {
    if (!req.body) {
        return res.sendStatus(400);
    }

    let postId;
    try {
        postId = getPostId(req.body.url)
    } catch (err) {
        res.sendStatus(404)
        return;
    }

    requestWallPostById(req, res, postId)
}

function requestWallPostById(req, res, postId) {
    const options = {
        url: req.body.url,
        error: '',
        photos: [],
    }

    if (postId) {
        getPost(token.accessToken, postId)
            .catch(err => {
                console.log(err)
                throw new Error('Произошла ошибка. Попробуйте позже.');
            })
            .then(findPhotos)
            .then(data => {
                options.photos = data
                res.render('index', options)
            })
            .catch(err => {
                options.error = err.message;
                res.render('index', options)
            })
    } else {
        options.error = 'Введённый адрес некорректен, попробуйте ещё раз';
        res.render('index', options)
    }
}

function getVkApiRequestString(accessToken, method, options = {}) {
    if (!options.hasOwnProperty('v')) {
        options['v'] = '5.52'
    }
    options['access_token'] = accessToken

    return buildUrl(`https://api.vk.com/method/${method}`, options)
}

function getPostId(url) {
    if (url === undefined) {
        throw new ReferenceError('The form must contain the \"url\" field.')
    }
    const regex = /wall(-?\d+_\d+)/
    const match = regex.exec(url);
    if (match && match.length >= 2) {
        return match[1]
    }
}

function getPost(accessToken, postId) {
    const options = {
        posts: postId,
        copy_history_depth: 0
    }

    return promiseRequest(
        getVkApiRequestString(accessToken, 'wall.getById', options),
        true
    )
        .then(data => data.response[0])
}

function findPhotos(post) {
    if (post === undefined) {
        throw new Error('Нет информации о посте. Возможно пост не существует или у вас нет к нему доступа.');
    }
    if (!post.hasOwnProperty('attachments')) {
        return []
    }

    return post.attachments
        .filter(attachment => attachment.type === 'photo')
        .map(attachment => attachment.photo)
        .map(findMaximumPhotoSize)
}

function findMaximumPhotoSize(photoObj) {
    const prefix = 'photo_';
    const maxSize = Math.max(
        ...Object.keys(photoObj)
            .filter(key => key.includes(prefix))
            .map(key => parseInt(key.slice(prefix.length)))
    )
    return photoObj[prefix + maxSize]
}

module.exports = {
    displayForm,
    requestWallPost,
}
