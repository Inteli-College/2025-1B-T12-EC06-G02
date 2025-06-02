import { create } from "zustand";

export const useDadosStore = create((set) => ({
  dados: [],
  setDados: (d) => set({ dados: d }),
}));