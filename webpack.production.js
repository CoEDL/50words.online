"use strict";

const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
    target: "web",
    mode: "production",
    entry: ["./src/vendor.js", "./src/index.js"],
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "[name].[fullhash].bundle.js",
    },
    // optimization: {
    //     minimize: true,
    //     minimizer: [new TerserPlugin()],
    // },
    plugins: [
        new CleanWebpackPlugin({
            cleanOnceBeforeBuildPatterns: ["*.js", "*.css", "*.LICENSE"],
        }),
        new MiniCssExtractPlugin(),
        new HtmlWebpackPlugin({
            title: "50words",
            template: "./src/index.html",
        }),
        new VueLoaderPlugin(),
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: "vue-loader",
            },
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            publicPath: "",
                        },
                    },
                    "css-loader",
                    "postcss-loader",
                ],
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            publicPath: "",
                        },
                    },
                    "css-loader",
                    "sass-loader",
                    "postcss-loader",
                ],
            },
            {
                test: /\.(woff|woff2|ttf|eot|svg|png|jp(e*)g|gif|mp4)?$/,
                loader: "file-loader",
                options: {
                    name: "assets/[contenthash].[ext]",
                    esModule: false,
                },
            },
        ],
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
            store: path.resolve(__dirname, "src/store"),
        },
    },
};
