"use strict";

import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);
import { loadWordData } from "./data-loader.service";

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
                    language: language.name,
                    lat: language.lat,
                    lng: language.lng
                };
            });
        },
        unsetSelectedWord(state) {
            state.selectedWord = undefined;
        },
        unsetSelectedLanguage(state) {
            state.selectedLanguage = undefined;
        },
        show(state, payload) {
            state.show = payload;
        },
        setPlayAll(state, payload) {
            // console.log(
            //     `old state: ${state.playAll.state}, new state: ${payload.state}`
            // );
            state.playAll = {
                ...state.playAll,
                ...payload
            };
        }
    },
    actions: {
        async loadWord({ state, commit }, payload) {
            // console.log("loadWord", JSON.stringify(payload, null, true));
            const word = await loadWordData({
                words: state.words,
                word: payload.word
            });
            console.log("Loaded data for word:", payload.word);
            if (payload.triggerPlayAll) {
                commit("setPlayAll", {
                    state: "next"
                });
            }
            commit("setSelectedWord", { word });
        }
    },
    getters: {}
};
export const store = new Vuex.Store(configuration);

function reset() {
    return {
        show: "languages",
        words: [],
        languages: [],
        selectedLanguage: undefined,
        selectedWord: undefined,
        playAll: { state: "ready", loop: false }
    };
}
