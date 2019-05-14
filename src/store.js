"use strict";

import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const configuration = {
    strict: process.env.NODE_ENV !== "production",
    state: reset(),
    mutations: {
        reset(state) {
            state = reset();
        },
        setWords(state, payload) {
            state.words = [...payload.words];
        },
        setLanguages(state, payload) {
            state.languages = [...payload.languages];
        },
        setSelectedLanguage(state, payload) {
            state.selectedLanguage = payload;
        },
        setSelectedWord(state, payload) {
            state.selectedWord = payload.word.map(w => {
                const language = state.languages.filter(
                    l => l.code === w.code
                )[0];
                return {
                    ...w,
                    lat: language.lat,
                    lng: language.lng
                };
            });
        },
        unsetSelectedWord(state) {
            state.selectedWord = undefined;
        }
    },
    getters: {}
};
export const store = new Vuex.Store(configuration);

function reset() {
    return {
        words: [],
        languages: [],
        selectedLanguage: {},
        selectedWord: undefined
    };
}
