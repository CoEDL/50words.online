"use strict";

import Vue from "vue";
import Vuex from "vuex";
import { flattenDeep } from "lodash";
Vue.use(Vuex);

const configuration = {
    strict: process.env.NODE_ENV !== "production",
    state: reset(),
    mutations: {
        reset(state) {
            state = reset();
        },
        setWords(state, payload) {
            state.words = { ...payload.words };
        },
        setLanguages(state, payload) {
            state.languages = [...payload.languages];
        },
        setSelectedLanguage(state, payload) {
            state.selectedLanguage = payload;
        }
    },
    getters: {}
};
export const store = new Vuex.Store(configuration);

function reset() {
    return {
        words: {},
        languages: [],
        selectedLanguage: {}
    };
}
