const path = require('path');

module.exports = {
    entry: {
        add_rate: path.resolve(__dirname, './frontend/src/add-rate/add-rate.js'),  // path to our input file
        discover: path.resolve(__dirname, './frontend/src/discover/discover.js'),
        entry_bootstrap: path.resolve(__dirname, './frontend/src/entry-bootstrap/entry-bootstrap.js')
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
            },
            {
                test: /\.js$/,
                enforce: 'pre',
                use: ['source-map-loader'],
            },
        ]
    },
    optimization: {
        chunkIds: 'named',
        splitChunks: {
            chunks: 'all',
            maxInitialRequests: Infinity,
            minSize: 0,
            cacheGroups: {
                react: {
                    test: /[\\/]node_modules[\\/]((?!(bootstrap|@popperjs)).*)[\\/]/,
                    name: 'react',
                },
                bootstrap: {
                    test: /[\\/]node_modules[\\/](bootstrap|@popperjs)[\\/]/,
                    name: 'bootstrap',
                },
                common: {
                    test: /[\\/]frontend[\\/]src[\\/]common[\\/]/,
                    name: 'common',
                }
            }
        },
    },
};