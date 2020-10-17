"use strict";

export async function loadLanguages() {
    const languages = await get("/repository/languages.json");
    return languages;
}

export async function loadWords() {
    let words = await get("/repository/words.json");
    return words;
}

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

export async function loadLanguageMetadata({ code }) {
    let response = await fetch(
        mapRepositoryRoot(`/repository/${code}/index.json`)
    );
    if (response.status !== 200) {
        throw new Error(response);
    }
    return await response.json();
}

export async function loadLanguageData({ code }) {
    const data = await loadLanguageMetadata({ code });

    data.words = data.properties.words
        .map((w) => {
            return {
                ...w,
                audio: mapRepositoryRoot(w.audio),
            };
        })
        .filter((w) => {
            return w?.audio?.length || w?.video?.length;
        });
    return data;
}

export async function loadWordData({ index }) {
    let words = await get(`/repository/${index}`);
    return words;
}

export async function loadProcessingData() {
    let response = await fetch(mapRepositoryRoot(`/repository/errors.json`));
    if (response.status !== 200) {
        throw new Error(response);
    }
    const errors = await response.json();

    // response = await fetch(
    //     mapRepositoryRoot(`/repository/gambay-additions.json`)
    // );
    // if (response.status !== 200) {
    //     throw new Error(response);
    // }
    // const additions = await response.json();
    return { errors };
}

export function mapRepositoryRoot(path) {
    return path;
    const root =
        process.env.NODE_ENV === "development"
            ? "/repository"
            : "/50words/repository";
    return path.replace("/repository", root);
}
