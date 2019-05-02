"use strict";

import { capitalize } from "lodash";

export async function loadData({ store }) {
    const dataFiles = ["words", "languages"];
    for (let file of dataFiles) {
        try {
            let response = await fetch(`/repository/${file}.json`);
            if (response.status !== 200) {
                throw new Error(response);
            }
            let data = await response.json();
            store.commit(`set${capitalize(file)}`, data);
        } catch (error) {
            console.log(error);
        }
    }
}

export async function loadLanguageData({ code }) {
    // console.log(`/repository/${code}/index.json`)
    let response = await fetch(`/repository/C20/index.json`);
    if (response.status !== 200) {
        throw new Error(response);
    }
    return await response.json();
}
