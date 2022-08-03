import { createRouter, createWebHistory } from "vue-router";
import ShellComponent from "components/Shell.component.vue";
import BadRequestComponent from "components/BadRequest.component.vue";
import AdminComponent from "components/Admin.component.vue";
import MobileRouteWrapperComponent from "components/MobileRouteWrapper.component.vue";
import PlayAllShellComponent from "components/PlayAllShell.component.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: ShellComponent,
        children: [],
    },
    {
        name: "playall",
        path: "/playall",
        component: PlayAllShellComponent,
    },
    {
        name: "about",
        path: "/about",
        component: MobileRouteWrapperComponent,
    },
    {
        name: "help",
        path: "/help",
        component: MobileRouteWrapperComponent,
    },
    {
        name: "contribute",
        path: "/contribute",
        component: MobileRouteWrapperComponent,
    },
    {
        name: "admin",
        path: "/admin",
        component: AdminComponent,
    },
];

const router = createRouter({
    history: createWebHistory("/"),
    routes,
});

export default router;
