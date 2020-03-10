<template>
  <div>
    <v-container>
      <v-layout>
        <v-flex xs12 md4>
          <v-card class="mx-auto" max-width="300px">
              <v-img :src="`data:image/jpeg;base64,${requestImage}`" class="request-image"></v-img>
              <hr/>
            <v-card-title>요청 이미지</v-card-title>
          </v-card>
        </v-flex>

        <v-flex xs12 md8>
          <v-data-table :headers="headers" :items="items" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer class="elevation-1">
            <template v-slot:item.imageData="{ item }">
              <v-img :src="`data:image/jpeg;base64,${item.imageData}`" class="result-image"></v-img>
            </template>
          </v-data-table>
          <div class="text-xs-center pt-2">
            <v-pagination v-model="page" :length="pageCount" circle></v-pagination>
          </div>
        </v-flex>
      
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  data(){
    return {
      page: 1,
      pageCount: 0,
      itemsPerPage: 5,
      headers:[
        { text:'상표이미지', value:'imageData', sortable: false },
        { text:'상표명', value:'title', sortable: false },
        { text:'출원상태', value:'applicationStatus', sortable: false },
        { text:'출원인이름', value:'applicantName', sortable: false },
        { text:'대리인이름', value:'agentName', sortable: false },
        { text:'공고일자', value:'publicationDate', sortable: false },
        { text:'공고번호', value:'publicationNumber', sortable: false },
      ],
      items:[],
    }
  },
  computed: {
    resultCount() {
      return this.$store.getters.getResultCount;
    },
    requestImage() {
      return this.$store.getters.getRequestImage;
    },
    resultImages() {
      return this.$store.getters.getResultImages;
    },
    resultInfos() {
      return this.$store.getters.getPatentInfos;
    }
  },
  created() {
    // initialize items
    for(let idx = 0; idx < this.resultCount; idx++) {
      const obj = {
        imageData: this.resultImages[idx],
        title: this.resultInfos[idx].title,
        applicationStatus: this.resultInfos[idx].applicationStatus,
        applicantName: this.resultInfos[idx].applicantName,
        agentName: this.resultInfos[idx].agentName,
        publicationDate: this.resultInfos[idx].publicationDate,
        publicationNumber: this.resultInfos[idx].publicationNumber,
      }

      this.items.push(obj);
    }

    // set page count
    this.pageCount = Math.ceil(this.resultImages.length / this.itemsPerPage);
  }
}
</script>

<style scoped>
.request-image {
  height: auto;
  width: 200px;
}
.result-image {
  height: auto;
  width: 200px;
}
</style>
