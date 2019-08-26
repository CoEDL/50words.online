s

> # Development of this application has moved to https://github.com/CoEDL/50words.online. 
> ## Issues raised here will be ignored.

# 50 Words
- [50 Words](#50-words)
  - [Updating the production dataset](#updating-the-production-dataset)
  - [Developing the application](#developing-the-application)
    - [Producing a data repository to work from in development](#producing-a-data-repository-to-work-from-in-development)
  - [Creating the repository data for the application](#creating-the-repository-data-for-the-application)
  - [Building production distributable](#building-production-distributable)
  - [Rebuilding and restarting the web container](#rebuilding-and-restarting-the-web-container)

This project aims to provide fifty words in every Indigenous language of Australia. We hope that this will be a useful resource for schools and educational organisations to learn 50 words in their local languages, and for the general public to discover the diversity of languages around Australia.

## Updating the production dataset

There are two steps involved. The first is to upload the data to the server and the second is to
run the extraction tool that creates the repository for the application.

Authorised people have access to the server via SSH - SCP then do the following:

```
> cd /srv/pdsc-50-words
> ./bin/update-data.sh --prod

```

**Watch the output of the script for yellow log lines (warnings - issues with the structure of an excel sheet) and red log lines
(errors).**

## Developing the application

To develop this application you will need a dataset that is not distributed with this repo (contact
Nick Thieberger - https://www.findanexpert.unimelb.edu.au/display/person18278). You will also need
a computer with nodejs and docker installed.

### Producing a data repository to work from in development

After you've received a dataset to work from create a folder `data` in the top level of the source code
and put the data in there. Then you can run the data extraction script to create a repository for the application viz:

```
> ./bin/update-data.sh --dev
```

After that, start the development server as:

```
> npm run develop
```

Then load `http://localhost:9001` in your browser.

## Creating the repository data for the application

The application data arrives as excel sheets that then need to be processed into json
data files that the application works from. The process is roughly as follows:

-   checkout source code repository onto a machine with docker installed
-   create a folder 'data' in the root of the repo
    -   in the data folder add the file 'AIATSIS-geography.xlsx'
    -   in the data folder create a folder for each language that contains the xls file and the audio / video files
-   run at the shell: `./bin/update-data.sh --dev`
    -   this will start a docker container that will process the data in the data folder and create a 'repository' structure in the 'dist' folder

By default, the script won't re-transcode files so that updates happen quickly. If you need to force
it (because you've updated the source audio files) then run at the shell: `./bin/update-data.sh --dev --update-all`

## Building production distributable

To build the production version of the application and deploy it do the following (on the 50words server)

```
update source
> cd /srv/pdsc-50-words
> git pull

build distributable
> npm run build

archive current version (just in case)
> \sudo rsync -av --exclude repository /srv/50words.online /srv/50words.online-$(date +%Y%m%d)

update application
> \sudo rsync -av --delete *.js --delete *.html --delete *.css dist/ /srv/50words.online/
```

## Rebuilding and restarting the web container

```
docker build --rm=true --tag "pdsc/50words.online" .
docker service update 50words_web --force
```
