import axios from "axios";

const apiClient = axios.create({
    baseURL: "https://fastapi.twnsnd.net",
    headers: {
        "Content-Type": "application/json",
    },
});

const api = {

    //example
    // async getUsers() {
    //     const response = await apiClient.get("/users");
    //     return response.data;
    // },

}

export default api;

//example on how to import and use
// import api from "@/api";
//
// async function loadUsers() {
//     try {
//         const users = await api.getUsers();
//         console.log(users);
//     } catch (err) {
//         console.error("Failed to load users:", err);
//     }
// }