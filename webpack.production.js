"use strict";

const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
    target: "web",
    mode: "production",
    devtool: "none",
    entry: ["./src/vendor.js", "./src/index.js"],
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "[name].[contenthash].bundle.js"
    },
    optimization: {
        moduleIds: "hashed",
        runtimeChunk: "single",
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: "vendors",
                    chunks: "all"
                }
            }
        },
        minimizer: [new TerserPlugin(), new OptimizeCSSAssetsPlugin({})]
    },
    plugins: [
        new CleanWebpackPlugin({
            cleanOnceBeforeBuildPatterns: ["*.js", "*.css", "*.LICENSE"]
        }),
        new MiniCssExtractPlugin({
            filename: "[name].[contenthash].css"
        }),
        new HtmlWebpackPlugin({
            title: "50words",
            template: "./src/index.html"
        }),
        new VueLoaderPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: "vue-loader"
            },
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: /node_modules/,
                query: { compact: false }
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, "css-loader"]
            },
            {
                test: /\.scss$/,
                use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
            },
            {
                test: /\.(woff|woff2|ttf|eot|svg|png|jp(e*)g|gif)?$/,
                loader: "file-loader?name=res/[name].[ext]?[hash]"
            }
        ]
    },
    resolve: {
        alias: {
            src: path.resolve(__dirname, "src"),
            assets: path.resolve(__dirname, "src/assets"),
            components: path.resolve(__dirname, "src/components"),
            configuration: path.resolve(__dirname, "src/configuration"),
            directives: path.resolve(__dirname, "src/directives"),
            routes: path.resolve(__dirname, "src/routes/"),
            services: path.resolve(__dirname, "src/services"),
            store: path.resolve(__dirname, "src/store")
        }
    }
};
