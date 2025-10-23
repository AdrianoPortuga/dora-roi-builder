import { api } from "./api";

export type VendorPayload = {
  name: string;
  country: string; // ISO2, ex: "BR", "PT", "US"
  criticality: "low" | "medium" | "high" | "Low" | "Medium" | "High";
};

export const listVendors   = async () => (await api.get("/")).data;
export const createVendor  = async (payload: VendorPayload) => (await api.post("/", payload)).data;
export const updateVendor  = async (id: number, payload: VendorPayload) => (await api.put(`/${id}`, payload)).data;
export const deleteVendor  = async (id: number) => (await api.delete(`/${id}`)).data;
