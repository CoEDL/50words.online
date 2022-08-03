import "regenerator-runtime";
import "@/assets/tailwind.css";
import "assets/global-styles.scss";
import "element-plus/theme-chalk/index.css";
import "mapbox-gl/dist/mapbox-gl.css";
import "@fortawesome/fontawesome-free/js/all";
import { config } from "@fortawesome/fontawesome-svg-core";
config.autoReplaceSvg = "nest";
import mapboxgl from "mapbox-gl";

// import VueAnalytics from "vue-analytics";

// const isProd = process.env.NODE_ENV === "production";
// Vue.use(VueAnalytics, {
//     id: "UA-36256674-2",
//     router,
//     debug: {
//         isProd: !isProd,
//         sendHitTask: isProd,
//     },
// });
// App.router = router;
// App.store = store;
// const app = new Vue(App);

import { createApp } from "vue";
import App from "./App.vue";
import router from "./routes";
import { store } from "./store";
import ElementPlus from "element-plus";

(async () => {
    // Vue.config.productionTip = false;

    const app = createApp(App);
    app.use(store);
    app.use(router);
    app.use(ElementPlus);
    app.mount("#app");
})();
