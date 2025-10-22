# Wayback-Public-Library
School Project MIS 565

### Client

1. go to client directory using `cd client`
2. make sure you have node and npm installed (this project uses 22). pro tip: Download node version manager if you want easier node/npm access.
3. run `npm install`
4. run `npm run dev` to start dev local dev server
5. if wanting to deploy to firebase make sure you add creds to client/src/firebase.js then follow steps 6-8
6. make sure you have firebase cli tools installed and run `firebase login`
7. auth into the firebase and then run `npm run build` to build the application
8. run `firebase deploy`