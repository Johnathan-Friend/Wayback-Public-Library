import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://wayback.twnsnd.net/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
})

//GET requests
const api = {
  async getAllItems() {
    try {
      const response = await apiClient.get('items/')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getItemDetails(itemDetailsId) {
    try {
      const response = await apiClient.get(`item-details/${itemDetailsId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getPatronDetails(patronId) {
    try {
      const response = await apiClient.get(`patrons/${patronId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getAllPatrons() {
    try {
      const response = await apiClient.get('patrons/')
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getPatronNumberOfBooksCheckedOut(patronId) {
    try {
      const response = await apiClient.get(`transactions/patron/${patronId}/count`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async checkInItem(patronId, itemId, returnDate) {
    try {
      const response = await apiClient.post('transactions/checkin', {
        patron_id: patronId,
        item_id: itemId,
        return_date: returnDate,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async updatePatronFee(patronId, newFee) {
    try {
      const response = await apiClient.put(`patrons/${patronId}`, {
        fee: newFee,
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getTransactionByItemId(itemId) {
    try {
      const response = await apiClient.get(`transactions/item/${itemId}`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  async getItemsNeedingReshelving() {
    try {
      const response = await apiClient.get(`items/needs_reshelving/`)
      return response.data
    } catch (error) {
      throw error
    }
  },

  //POST requests
  async checkOutItem(patronID, itemID) {
    try {
      const response = await apiClient.post(
        'transactions/check-out-item',
        {},
        {
          params: {
            patron_id: patronID,
            item_id: itemID,
          },
        },
      )
      return { data: response.data, status: 200 }
    } catch (error) {
      if (error.status === 400 && error.response?.data?.detail) {
        return { data: error.response?.data?.detail, status: 400 }
      }
      throw error
    }
  },

  async reshelveItem(item_id) {
    try {
      const response = await apiClient.post(`items/reshelve/${item_id}`)
      return { data: response.data, status: 200 }
    } catch (error) {
      if (error.status === 400 && error.response?.data?.detail) {
        return { data: error.response?.data?.detail, status: 400 }
      }
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
    },

    //PATCH requests
    async updatePatronFee(patronId, newFee) {
        try {
            const response = await apiClient.patch(`patrons/${patronId}`, {
                 FeeBalance: newFee
            });
            return response.data;
        }
        catch (error) {
            throw error;
        }
    },

    async extendMembership(patronId, newMembershipExpirationDate) {
        try {
            const response = await apiClient.patch(`patrons/${patronId}`, {
                MembershipExpiration: newMembershipExpirationDate
            });
            return response.data;
        }
        catch (error) {
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
    },

    // Patron management
    async createPatron(firstName, lastName) {
        try {
            const response = await apiClient.post('patrons/', {
                FirstName: firstName,
                LastName: lastName
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async updatePatron(patronId, updateData) {
        try {
            const response = await apiClient.patch(`patrons/${patronId}`, updateData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    async deletePatron(patronId) {
        try {
            const response = await apiClient.delete(`patrons/${patronId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default api

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
