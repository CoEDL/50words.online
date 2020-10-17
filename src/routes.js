"use strict";

import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

import ShellComponent from "components/Shell.component.vue";
import BadRequestComponent from "components/BadRequest.component.vue";
import AdminComponent from "components/Admin.component.vue";
import MobileRouteWrapperComponent from "components/MobileRouteWrapper.component.vue";
import PlayAllShellComponent from "components/PlayAllShell.component.vue";

export const router = new VueRouter({
    mode: "history",
    base: process.env.NODE_ENV === "development" ? "/" : "/staging/",
    routes: [
        { path: "*", name: "404", component: BadRequestComponent },
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
    ],
});
