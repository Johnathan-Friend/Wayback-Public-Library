import axios from "axios";

const apiClient = axios.create({
    baseURL: "https://wayback.twnsnd.net/api/v1/",
    headers: {
        "Content-Type": "application/json",
    },
});

const api = {
    async getAllItems() {
        try {
            const response = await apiClient.get('items/');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async getItemDetails(itemDetailsId) {
        try {
            const response = await apiClient.get(`item-details/${itemDetailsId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async getPatronDetails(patronId) {
        try {
            const response = await apiClient.get(`patrons/${patronId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async getAllPatrons() {
        try {
            const response = await apiClient.get('patrons/');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async getPatronNumberOfBooksCheckedOut(patronId) {
        try {
            const response = await apiClient.get(`transactions/patron/${patronId}/count`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async checkInItem(patronId, itemId, returnDate) {
        try {
            const response = await apiClient.post('transactions/checkin', {
                patron_id: patronId,
                item_id: itemId,
                return_date: returnDate
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
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