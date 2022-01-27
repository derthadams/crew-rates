const path = require('path');
const common = require('./webpack.common');
const { merge } = require('webpack-merge');
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
// const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = merge(common, {
    mode: "production",
    output: {
        filename: '[name].bundle.js',  // output bundle file name
        path: path.resolve(__dirname, './frontend/static/rates/js/'),  // path to our Django static directory
    },
    module: {
        rules: [
            {
                test: /\.(css|scss)$/,
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
            }
        ]
    },
    optimization: {
        minimizer: [
            new OptimizeCssAssetsPlugin(),
            new TerserPlugin(),
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].css"
        }),
        new CleanWebpackPlugin(),
        // new HtmlWebpackPlugin({ // Can declare more than once to generate multiple html files
        //     template: "./src/template.ejs",
        //     filename: "../react_site.html",
        //     scriptLoading: 'defer',
        //     inject: false,
        //     minify: {
        //         removeAttributeQuotes: true,
        //         collapseWhitespace: true,
        //         removeComments: true
        //     },
        //     chunks: ['index']
        // }),
        // new HtmlWebpackPlugin({ // Can declare more than once to generate multiple html files
        //     template: "./src/base_template.ejs",
        //     filename: "../base.html",
        //     scriptLoading: 'defer',
        //     inject: false,
        //     minify: {
        //         removeAttributeQuotes: true,
        //         collapseWhitespace: true,
        //         removeComments: true
        //     },
        //     chunks: ['base']
        // })
    ],
});