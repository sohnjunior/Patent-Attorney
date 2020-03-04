<template>
  <div class="app">
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
            <v-pagination v-model="page" :length="pageCount"></v-pagination>
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
      pageCount: 3,
      itemsPerPage: 5,
      headers:[
        { text:'상표이미지', value:'imageData' },
        { text:'상표명', value:'title' },
        { text:'출원인이름', value:'applicantName' },
        { text:'대리인이름', value:'agentName' },
        { text:'출원상태', value:'applicationStatus' },
        { text:'공고일자', value:'publicationDate' },
        { text:'공고번호', value:'publicationNumber' },
      ],
      items:[],
    }
  },
  computed: {
    requestImage() {
      return this.$store.getters.getRequestImage;
    },
    resultImages() {
      return this.$store.getters.getResultImages;
    },
  },
  created() {
    // initialize items
    for(var image of this.resultImages) {
      const obj = {
        imageData: image,
        title:'s',
        applicantName:'a',
        agentName: 'm',
        applicationStatus:'p',
        publicationDate:'l',
        publicationNumber:'e'
      }
      this.items.push(obj);
    }
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
