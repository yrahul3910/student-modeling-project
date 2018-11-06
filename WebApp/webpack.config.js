const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    mode: "development",
    devtool: "inline-source-map",
    entry: [
        "babel-polyfill",
        path.resolve(__dirname, "src/index")
    ],
    output: {
        path: path.resolve(__dirname, "dist"),
        publicPath: "/",
        filename: "bundle.js"
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "src/index.html",
            inject: true
        })
    ],
    module: {
        rules: [
            {test: /\.jsx$/, exclude: /node_modules/, use: "babel-loader"},
            {test: /\.js$/, exclude: /node_modules/, use: "babel-loader"},
            {test: /\.css$/, use: [
                {
                    loader: "style-loader"
                },
                {
                    loader: "css-loader"
                }]},
            {test: /\.sass$/, use: "sass-loader"}
        ]
    }
};
