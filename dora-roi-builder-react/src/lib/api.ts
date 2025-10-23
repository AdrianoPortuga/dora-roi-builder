import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL;
if (!baseURL) {
  // ajuda no diagnÃ³stico
  console.error("VITE_API_URL nÃ£o definido. Verifique .env do front.");
}

export const api = axios.create({
  baseURL,                 // ex.: http://127.0.0.1:8000/api/v1
  withCredentials: true,   // se o back usa cookies para sessÃ£o/JWT
  timeout: 15000,
});

// log Ãºtil na inicializaÃ§Ã£o
console.log("[API] baseURL =", baseURL);
