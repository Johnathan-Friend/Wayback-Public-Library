# Wayback-Public-Library
School Project MIS 565

### Client

1. go to client directory using `cd client`
2. make sure you have node and npm installed (this project uses 22). pro tip: Download node version manager if you want easier node/npm access.
3. run `npm install`
4. run `npm run dev` to start dev local dev server
5. if wanting to deploy to firebase make sure you add creds to client/src/firebase.js then follow steps 6-8 (but shouldn't need to, we will do every few days deployment based off of main)
6. make sure you have firebase cli tools installed and run `firebase login`
7. auth into the firebase and then run `npm run build` to build the application
8. run `firebase deploy`

##### Components

- CRUD actions table (can add, delete, read, update table information)
  - https://vuetifyjs.com/en/components/data-tables/basics/#crud-actions
- Basic table with pagination
  - https://vuetifyjs.com/en/components/data-tables/basics/#usage
- Standalone Forms
  - https://vuetifyjs.com/en/components/forms/#rules
- Date pickers
  - https://vuetifyjs.com/en/components/date-pickers/#usage

##### Best Practices

- use the api/api.js to use axios and make reusable queries
- only full routes or pages go into the /views directory
- components that go into views go into the /components directory
- site wide styling goes into assets/main.css