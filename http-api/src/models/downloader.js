const fs = require('fs');
const path = require('path');
const request = require('request');
const nodeZip = require('node-zip');

class Downloader {
    constructor(urls, downloadsFolder, archiveName) {
        this.urls = urls
            .map(url => url.split(/[?#]/)[0])
            .map(url => url.endsWith('/') ? url.slice(0, -1) : url);
        this.folder = downloadsFolder;
        this.archiveName = archiveName;
    }

    saveFiles() {
        return Promise.all(this.urls.map((url, index) => {
            const filename = path.join(this.folder, index + path.extname(url))
            return this.downloadPromise(url, filename)
        }))
            .then(this.archiveFiles.bind(this))
    }

    downloadPromise(url, filename) {
        return new Promise((resolve, reject) => {
            request
                .get(url)
                .on('response', function (response) {
                    console.log(response.statusCode, response.headers['content-type'])
                })
                .pipe(fs.createWriteStream(filename))
                .on('finish', () => {
                    resolve(filename)
                })
                .on('error', function (err) {
                    reject(err)
                })
        })
    }

    archiveFiles(files) {
        const zip = new nodeZip();
        for (let file of files) {
            const img = fs.readFileSync(file);
            zip.file(path.basename(file), img);
        }

        const data = zip.generate({base64: false, compression: 'DEFLATE'});
        fs.writeFileSync(path.join(this.folder, this.archiveName), data, 'binary');

        return path.join(this.folder, this.archiveName);
    }
}

module.exports = Downloader;
