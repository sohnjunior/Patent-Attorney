<template>
  <div>
    <v-data-table :headers="headers" :items="items" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer class="elevation-1">
    <template v-slot:item.imageData="{ item }">
      <v-img :src="`data:image/jpeg;base64,${item.imageData}`" class="result-image"></v-img>
    </template>
    </v-data-table>
    <div class="text-xs-center pt-2">
      <v-pagination v-model="page" :length="pageCount" circle></v-pagination>
    </div>
  </div>
</template>

<script>
export default {
  props: { 'items': Array, 'pageCount': Number, 'itemsPerPage': Number },
  data(){
    return {
      page: 1,
      headers:[
        { text:'상표이미지', value:'imageData', sortable: false },
        { text:'상표명', value:'title', sortable: false },
        { text:'출원상태', value:'applicationStatus', sortable: false },
        { text:'출원인이름', value:'applicantName', sortable: false },
        { text:'대리인이름', value:'agentName', sortable: false },
        { text:'공고일자', value:'publicationDate', sortable: false },
        { text:'공고번호', value:'publicationNumber', sortable: false },
      ],
    }
  },
}
</script>

<style>
.result-image {
  height: auto;
  width: 200px;
}
</style>