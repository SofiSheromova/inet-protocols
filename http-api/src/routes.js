const {error404} = require('./controllers/errors');
const {requestWallPost, displayForm} = require('./controllers/form');
const {authorize, createToken} = require('./controllers/token')
const {downloadAndArchive} = require('./controllers/download')

module.exports = (app) => {
    app.get('/', authorize);

    app.get('/code', createToken);

    app
        .route('/form')
        .get(displayForm)
        .post(requestWallPost)

    app.post('/download', downloadAndArchive)

    app.all('*', error404);
}
