module.exports = {
    future: {},
    mode: "jit",
    content: ["./public/index.html", "./src/**/*.html", "./src/**/*.{js,jsx,ts,tsx,vue}"],
    theme: {
        extend: {
            colors: {
                highlight: {
                    dark: "#c44d2b",
                    light: "#e9b69e",
                },
            },
        },
        screens: {
            sm: "640px",
            md: "768px",
            lg: "1024px",
            xl: "1280px",
            xxl: "1600px",
        },
    },
    variants: {},
    plugins: [],
};
