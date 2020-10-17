module.exports = {
    variants: {
        textColor: ["responsive", "hover", "focus", "group-hover"],
    },
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
};
