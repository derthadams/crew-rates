const path = require('path');
const common = require('./webpack.common');
const { merge } = require('webpack-merge');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const {CleanWebpackPlugin} = require("clean-webpack-plugin");

module.exports = merge(common, {
    mode: "development",
    output: {
        filename: '[name].bundle.js',  // output bundle file name
        path: path.resolve(__dirname, './frontend/static/rates/js/'),  // path to our Django static directory
        publicPath: './static/'
    },
    module: {
        rules: [
            {
                test: /\.(css|scss)$/i,
                use: [
                    {loader: MiniCssExtractPlugin.loader},
                    {loader: "css-loader"},
                    {loader: "postcss-loader",
                        options: {
                            postcssOptions: {
                                plugins: function() {
                                    return [
                                        require('autoprexifer')
                                    ];
                                }
                            }
                        }
                    },
                    {loader: "sass-loader"},
                ]
            },
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].css"
        }),
        new CleanWebpackPlugin(),
    ]
});