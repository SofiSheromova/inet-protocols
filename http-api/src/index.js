const path = require('path')

const express = require('express');
const morgan = require('morgan')
const exphbs = require('express-handlebars');
const bodyParser = require('body-parser')

const routes = require('./routes')
const config = require('config')

const app = express();

const hbs = exphbs.create({
    defaultLayout: 'main',
    extname: 'hbs'
});

const viewsDir = path.join(__dirname, 'views');
const partialsDir = path.join(viewsDir, 'partials');
const publicDir = path.join(__dirname, 'public');

app.engine('hbs', hbs.engine);

app.set('view engine', 'hbs');
app.set('views', viewsDir);

if (config.get('debug')) {
    app.use(morgan('dev'));
}

app.use(express.urlencoded({extended: true}));

app.use(express.static(publicDir));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use((err, _req, _res, next) => {
    console.error(err.stack);
    next();
});

routes(app)

const port = config.get('port');
app.listen(port, () => {
    console.info(`Server started on ${port}`);
    console.info(`Open http://localhost:${port}/`);
});
