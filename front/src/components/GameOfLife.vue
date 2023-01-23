<template>
  <div>
    <p v-if="err">{{ err }}</p>
    <table class="table" v-else>
      <tbody>
      <tr v-for="y in height" :key="y">
        <td v-for="x in width" :key="x" :class="{ 'alive': isCoord(x-1, y-1)?.alive }">
        </td>
      </tr>
      </tbody>
    </table>
    <button @click="nextGeneration()">Next</button>
  </div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  data() {
    return {
      err: null,
    }
  },
  mounted() {
    this.nextGeneration()
  },

  computed: {
    ...mapGetters({
      cells: 'cells/cells',
      width: 'cells/width',
      height: 'cells/height'
    }),
  },
  methods: {
    isCoord(x, y) {
      return this.cells.find(c => c.x == x && c.y == y);
    },

    async nextGeneration() {
      try {
        await this.$store.dispatch("cells/nextGeneration");
        this.err = null
      } catch (error) {
        this.err = error.response.data
      }
    }
  }
}

</script>

<style>
.table td {
  width: 20px;
  height: 20px;
  background-color: #a72870;
}

.alive {
  background-color: #28a745 !important;
}
</style>
