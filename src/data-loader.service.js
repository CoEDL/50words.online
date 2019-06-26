"use strict";

import { compact, orderBy } from "lodash";

export async function loadData({ store }) {
    const words = (await get(mapRepositoryRoot("/repository/words.json")))
        .words;
    store.commit(`setWords`, { words });
    let languages = (await get(mapRepositoryRoot("/repository/languages.json")))
        .languages;
    store.commit(`setLanguages`, { languages });

    async function get(path) {
        try {
            let response = await fetch(path);
            if (response.status !== 200) {
                throw new Error(response);
            }
            return await response.json();
        } catch (error) {
            console.log(error);
            return [];
        }
    }
}

export async function loadLanguageData({ code }) {
    let response = await fetch(
        mapRepositoryRoot(`/repository/${code}/index.json`)
    );
    if (response.status !== 200) {
        throw new Error(response);
    }
    let data = await response.json();
    data.words = data.properties.words.map(w => {
        return {
            ...w,
            audio_file: mapRepositoryRoot(w.audio_file)
        };
    });
    return data;
}

export async function loadWordData({ word, words }) {
    let index = words.filter(w => {
        return w.name === word;
    })[0].index;
    let response = await fetch(mapRepositoryRoot(`/repository/${index}`));
    if (response.status !== 200) {
        throw new Error(response);
    }
    word = await response.json();
    word = word.map(w => {
        return {
            ...w,
            audio_file: mapRepositoryRoot(w.properties.audio_file)
        };
    });
    return word;
}

export async function loadProcessingData() {
    let response = await fetch(mapRepositoryRoot(`/repository/errors.json`));
    if (response.status !== 200) {
        throw new Error(response);
    }
    const errors = await response.json();

    response = await fetch(
        mapRepositoryRoot(`/repository/gambay-additions.json`)
    );
    if (response.status !== 200) {
        throw new Error(response);
    }
    const additions = await response.json();
    return { errors, additions };
}

export function mapRepositoryRoot(path) {
    return path;
    const root =
        process.env.NODE_ENV === "development"
            ? "/repository"
            : "/50words/repository";
    return path.replace("/repository", root);
}
