import { createStore } from "vuex";

import { loadLanguages, loadWords, loadWordData, loadLanguageData } from "./data-loader.service";
import { cloneDeep, orderBy } from "lodash";

export const mutations = {
    reset(state) {
        state = reset();
    },
    setWords(state, payload) {
        state.words = [...payload.words];
    },
    setLanguages(state, payload) {
        state.languages = orderBy(payload.languages, (l) => l.properties.name);
    },
    setSelectionToDisplay(state, payload) {
        state.selection = { ...payload };
    },
    setLayer(state, payload) {
        state.layer = payload;
    },
    flyTo(state, payload) {
        state.flyTo = { ...payload };
    },
};

export const actions = {
    async loadData({ commit }) {
        let response = await loadLanguages();
        commit("setLanguages", response);

        response = await loadWords();
        commit("setWords", response);
    },
    async loadWord({ state, commit }, word) {
        const words = await loadWordData({ index: word.index });

        commit("setLayer", "words");
        commit("setSelectionToDisplay", {
            type: "word",
            data: { ...word, words },
        });
    },
    async loadLanguage({ state, commit }, { code }) {
        const data = await loadLanguageData({ code });

        commit("setLayer", "languages");
        commit("setSelectionToDisplay", {
            type: "language",
            data,
        });
    },
};

export const getters = {
    getWordList: (state) => () => {
        return cloneDeep(state.words);
    },
    // getSelectedWord: (state) => () => {
    //     return cloneDeep(state.selectedWord);
    // },
    getSelection: (state) => () => {
        return cloneDeep(state.selection);
    },
    getSelectionData: (state) => () => {
        return cloneDeep(state.selection.data);
    },
};

export const store = new createStore({
    strict: process.env.NODE_ENV !== "production",
    state: resetState(),
    getters,
    mutations,
    actions,
});

function resetState() {
    return {
        iOS:
            [
                "iPad Simulator",
                "iPhone Simulator",
                "iPod Simulator",
                "iPad",
                "iPhone",
                "iPod",
            ].includes(navigator.platform) ||
            // iPad on iOS 13 detection
            (navigator.userAgent.includes("Mac") && "ontouchend" in document),
        words: [],
        languages: [],
        layer: "languages",
        flyTo: undefined,
        selection: {
            type: undefined,
            data: undefined,
        },
    };
}
