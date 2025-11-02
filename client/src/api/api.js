import axios from "axios";

const apiClient = axios.create({
    baseURL: "https://wayback.twnsnd.net/api/v1/",
    headers: {
        "Content-Type": "application/json",
    },
});

const api = {

    //GET requests
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

    //POST requests
    async checkOutItem(patronID, itemID) {
        try {
            const response = await apiClient.post('transactions/check-out-item', {}, { 
                params: {
                    patron_id: patronID,
                    item_id: itemID
                }
            });
            return { data: response.data, status: 200 };
        } catch (error) {
            if (error.status === 400 && error.response?.data?.detail) {
                return { data: error.response?.data?.detail, status: 400 };
            }
            throw error;
        }
    },

    //DELETE requests
    async deleteTransaction(transactionID) {
        try {
            const response = await apiClient.delete(`transactions/${transactionID}`);
            return { data: response.data, status: 200 };
        } catch (error) {
            if (error.status === 400 && error.response?.data?.detail) {
                return { data: error.response?.data?.detail, status: 400 };
            }
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