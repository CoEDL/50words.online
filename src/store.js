"use strict";

import Vue from "vue";
import Vuex from "vuex";
import { flattenDeep } from "lodash";
Vue.use(Vuex);

const configuration = {
    strict: process.env.NODE_ENV !== "production",
    state: {},
    mutations: {
        reset(state) {
            state = {};
        }
    },
    getters: {}
};
export const store = new Vuex.Store(configuration);
