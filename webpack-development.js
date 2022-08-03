const path = require("path");
const { merge } = require("webpack-merge");
const common = require("./webpack-common");

const configuration = merge(common, {
    mode: "development",
    devtool: "eval-source-map",
    devServer: {
        static: [
            {
                directory: path.join(__dirname, "dist"),
            },
            {
                directory: path.join(__dirname, "data"),
                publicPath: "/repository",
            },
        ],
        compress: true,
        host: "0.0.0.0",
        port: 9000,
        historyApiFallback: true,
        hot: true,
    },
});

module.exports = configuration;
