"use strict";

import { compact, orderBy } from "lodash";

export async function loadData({ store }) {
    const words = (await get(mapRepositoryRoot("/repository/words.json")))
        .words;
    store.commit(`setWords`, { words });
    let languages = (await get(mapRepositoryRoot("/repository/languages.json")))
        .languages;
    languages = compact(
        languages.map(l => {
            return l.words ? l : undefined;
        })
    );
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
    data.words = data.words.map(w => {
        return {
            ...w,
            audio_file: mapRepositoryRoot(w.audio_file)
        };
    });
    return data;
}

export async function loadWordData({ index }) {
    let response = await fetch(mapRepositoryRoot(`/repository/${index}`));
    if (response.status !== 200) {
        throw new Error(response);
    }
    let word = orderBy(await response.json(), "language");
    word = word.map(w => {
        return {
            ...w,
            audio_file: mapRepositoryRoot(w.audio_file)
        };
    });
    return word;
}

export function mapRepositoryRoot(path) {
    const root =
        process.env.NODE_ENV === "development"
            ? "/repository"
            : "/50words/repository";
    return path.replace("/repository", root);
}
