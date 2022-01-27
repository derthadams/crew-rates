const path = require('path');

module.exports = {
    entry: {
        add_rate: './frontend/src/add-rate.js',  // path to our input file
        entry_bootstrap: './frontend/src/entry-bootstrap.js'
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
            }
        },
    },
};