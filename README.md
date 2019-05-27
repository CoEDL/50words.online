# 50 Words

- [50 Words](#50-words)
  - [Developing the application](#developing-the-application)
  - [Creating the repository data for the application](#creating-the-repository-data-for-the-application)
        This is a collection viewer designed specifically for use on repatriation devices.

It features:

-   modern tooling
-   a modern framework - Vue.js
-   modern styling designed specifically for non technical users and mobile devices

## Developing the application

To develop this application you will need nodejs installed. Then do:

```
> npm run develop
```

Then load `http://localhost:9000` in your browser.

## Creating the repository data for the application

The application data arrives as excel sheets that then need to be processed into json
data files that the application works from. The process is roughly as follows:
- checkout source code repository onto a machine with docker installed
- create a folder 'data' in the root of the repo
  - in the data folder add the file 'AIATSIS-geography.xlsx'
  - in the data folder create a folder for each language that contains the xls file and the audio / video files
- run at the shell: `docker-compose up`
  - this will start a docker container that will process the data in the data folder and create a 'repository' structure in the 'dist' folder
- copy the repository folder over to the app deployment folder of the language archives server