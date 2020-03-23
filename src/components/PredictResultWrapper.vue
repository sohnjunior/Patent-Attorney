<template>
  <v-app>
    <v-content>
      <v-container>
        <QueryImage></QueryImage>
      </v-container>
      <v-container>
        <ResultTable :items="items" :pageCount="pageCount" :itemsPerPage="itemsPerPage"></ResultTable>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { EventBus } from '../utils/event_bus.js';
import QueryImage from './QueryImage.vue';
import ResultTable from './ResultTable.vue';

export default {
  components: { QueryImage, ResultTable },
  data(){
    return {
      itemsPerPage: 5,
      pageCount: 5,
      items:[],
    }
  },
  computed: {
    // computed 속성에서 인자를 받아야 할 경우 이런식으로 가능
    resultCount() {
      return (idx) => {
        return this.$store.getters.getResultCount(idx);
      }
    },
    resultImages() {
      return (idx) => {
        return this.$store.getters.getResultImages(idx);
      }
    },
    resultInfos() {
      return (idx) => {
        return this.$store.getters.getPatentInfos(idx);
      }
    }
  },
  created() {
    EventBus.$on('index-change', (idx) => {
      this.items = [];
      const queryIdx = idx;
      for(let idx = 0; idx < this.resultCount(queryIdx); idx++) {
        const obj = {
          imageData: this.resultImages(queryIdx)[idx],
          title: this.resultInfos(queryIdx)[idx].title || this.resultInfos(queryIdx)[idx].articleName,
          applicationStatus: this.resultInfos(queryIdx)[idx].applicationStatus,
          applicantName: this.resultInfos(queryIdx)[idx].applicantName,
          agentName: this.resultInfos(queryIdx)[idx].agentName,
          publicationDate: this.resultInfos(queryIdx)[idx].publicationDate,
          publicationNumber: this.resultInfos(queryIdx)[idx].publicationNumber,
        }

        this.items.push(obj);
      }
      
      // set page count
      this.pageCount = Math.ceil(this.resultImages(queryIdx).length / this.itemsPerPage);
    });
  },
  mounted() {
    EventBus.$emit('index-change', 0);  // 초기 인덱스 0으로 설정
  }
}
</script>

<style>
</style>
