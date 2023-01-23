import {api} from "../api";

export default {
    namespaced: true,

    state: {
        cells: [],
        width: 0,
        height: 0
    },

    actions: {
       async nextGeneration({ commit }) {
            const response = await api.get("next_generation/");
            await commit("UPDATE_CELLS", response.data);
            await commit("UPDATE_WIDTH", response.data);
            await commit("UPDATE_HEIGHT", response.data);
        }
    },
    mutations: {
        UPDATE_CELLS: (state, payload) => {
            console.log(payload)
            state.cells = payload.alive_cells;
        },
        UPDATE_WIDTH: (state, payload) => {
            state.width = payload.width;
        },
        UPDATE_HEIGHT: (state, payload) => {
            state.height = payload.height;
        }
    },

    getters: {
        cells: (state) => state.cells,
        width: (state) => state.width,
        height: (state) => state.height,
    },
}