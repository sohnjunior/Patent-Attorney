<template>
  <div>
    <v-data-table :headers="headers" :items="items" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer class="elevation-1 custom-class">
    <template v-slot:item.imageData="{ item }">
      <v-img :src="item.imagePath" class="result-image"></v-img>
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
        { text:'상표이미지', value:'imageData', sortable: false, class: 'success--text subtitle-1', align:'center' },
        { text:'상표명', value:'title', sortable: false, class: 'success--text subtitle-1', align:'center' },
        { text:'출원상태', value:'applicationStatus', sortable: false, class: 'success--text subtitle-1', width: "100", align:'center' },
        { text:'출원인이름', value:'applicantName', sortable: false, class: 'success--text subtitle-1', width: "120", align:'center' },
        { text:'대리인이름', value:'agentName', sortable: false, class: 'success--text subtitle-1', align:'center' },
        { text:'공고일자', value:'publicationDate', sortable: false, class: 'success--text subtitle-1', align:'center' },
        { text:'공고번호', value:'publicationNumber', sortable: false, class: 'success--text subtitle-1', align:'center' },
      ],
    }
  },
}
</script>

<style scoped>
.table-title {
  color: rgb(255, 127, 165);
}

.result-image {
  height: auto;
  width: 200px;
}
</style>