import "regenerator-runtime";
import { mutations, getters, actions, store } from "./store";
import { loadLanguages, loadWords, loadWordData } from "./data-loader.service";
import { isArray } from "lodash";
import { readJson } from "fs-extra";
import path from "path";
import fetchMock from "jest-fetch-mock";
fetchMock.enableMocks();

import Vue from "vue";
import Vuex from "vuex";
Vue.config.productionTip = false;
Vue.config.devtools = false;
Vue.use(Vuex);

let state = {};

beforeEach(() => {
    fetch.resetMocks();

    state = {
        show: "languages",
        words: [],
        languages: [],
        selectedLanguage: undefined,
        selectedWord: undefined,
    };
});
test("test loading language data", async () => {
    const languages = await readJson(
        path.join("dist", "repository", "languages.json")
    );
    fetch.mockResponseOnce(JSON.stringify(languages));

    const response = await loadLanguages();
    expect("languages" in response).toBeTrue;
    expect(isArray(response.languages)).toBeTrue;

    mutations.setLanguages(state, response);
    expect(state.languages).toEqual(response.languages);
});

test("test loading words data", async () => {
    const words = await readJson(path.join("dist", "repository", "words.json"));
    fetch.mockResponseOnce(JSON.stringify(words));

    const response = await loadWords();
    expect("words" in response).toBeTrue;
    expect(isArray(response.words)).toBeTrue;

    mutations.setWords(state, response);
    expect(state.words).toEqual(response.words);
});

test("loading specific word data", async () => {
    const languages = await readJson(
        path.join("dist", "repository", "languages.json")
    );
    fetch.mockResponseOnce(JSON.stringify(languages));
    let response = await loadLanguages();
    mutations.setLanguages(state, response);

    const words = await readJson(path.join("dist", "repository", "words.json"));
    fetch.mockResponseOnce(JSON.stringify(words));
    response = await loadWords();
    mutations.setWords(state, response);

    let index = response.words.filter((w) => {
        return w.name === "hand";
    })[0].index;
    let word = await readJson(path.join("dist", "repository", index));
    fetch.mockResponseOnce(JSON.stringify(word));

    const wordIndex = await loadWordData({
        word: "hand",
        words: response.words,
    });
    expect(isArray(wordIndex)).toBeTrue;
    word = wordIndex[0];
    expect(word.type).toBe("Feature");
    expect(word.geometry.type).toBe("Point");

    mutations.setSelectedWord(state, { word: wordIndex });
    expect(state.selectedWord).toEqual(wordIndex);
});
