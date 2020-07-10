const Downloader = require('../models/downloader')
const path = require('path')

function downloadAndArchive(req, res) {
    if (!req.body || !req.body.hasOwnProperty('urls')) {
        return res.sendStatus(400);
    }

    const urls = req.body.urls;
    const downloadFolder = 'uploadedImages';
    const downloadPath = path.join(__dirname, '..', 'public', downloadFolder)
    const archiveName = 'photo.zip'

    new Downloader(urls, downloadPath, archiveName).saveFiles()
        .then(() => res.json({folder: downloadFolder, archiveName: archiveName}))
        .catch(err => res.json({error: err}))
}

module.exports = {
    downloadAndArchive,
}
