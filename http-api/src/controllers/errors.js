// Код «404 Not Found» отправляют в ответ на отсутствующий HTTP-ресурс
const error404 = (_req, res) => {
    res.sendStatus(404);
};

module.exports = {error404}
