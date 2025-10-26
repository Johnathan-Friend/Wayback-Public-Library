import axios from "axios";

const api = axios.create({
    baseURL: 'https://fastapi.twnsnd.net'
});

export default api;

```
Example: of how to call API

import api from "@/api";

async function getUsers() {
  const response = await api.get("/users");
  console.log(response.data);
}
```