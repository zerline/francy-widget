var path = require('path');
var version = require('./package.json').version;

var rules = [
    { test: /\.css$/, use: ['style-loader', 'css-loader']},
    { test: /\.(jpg|png|gif)$/, use: ['url-loader']}
]
var externals = ['@jupyter-widgets/base', '@jupyter-widgets/controls']

module.exports = [
    {// Notebook extension
        entry: './lib/extension.js',
        output: {
            filename: 'extension.js',
            path: path.resolve(__dirname, '..', 'sage-francy', 'static'),
            libraryTarget: 'amd'
        }
    },
    {// sage-francy bundle for the notebook
        entry: './lib/index.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, '..', 'sage-francy', 'static'),
            libraryTarget: 'amd'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: externals
    },
    {// embeddable sage-francy bundle
        entry: './lib/embed.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, 'dist'),
            libraryTarget: 'amd',
            publicPath: 'https://unpkg.com/sage-francy@' + version + '/dist/'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: externals
    }
];
