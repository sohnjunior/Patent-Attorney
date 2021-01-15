<template>
  <div>
    <v-data-table :headers="headers" :items="items" :page.sync="page" :items-per-page="itemsPerPage" hide-default-footer class="elevation-1 table-style">
    <template v-slot:item.imageData="{ item }">
      <v-img
        :lazy-src="require('../images/loading.png')"
        :src="item.imagePath"
        class="result-image">
        <template v-slot:placeholder>
            <v-row
              class="fill-height ma-0"
              align="center"
              justify="center"
            >
            <v-progress-circular indeterminate color="blue lighten-3"></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </template>
    </v-data-table>
    <div class="text-xs-center pt-2">
      <v-pagination v-model="page" :length="pageCount" circle color="blue accent-1"></v-pagination>
    </div>
  </div>
</template>

<script>
export default {
  props: {  'items': Array, 'pageCount': Number, 'itemsPerPage': Number },
  data(){
    return {
      page: 1,
      headers:[
        { text:'상표이미지', value:'imageData', sortable: false, class: 'white--text subtitle-1', align:'center' },
        { text:'상표명', value:'title', sortable: false, class: 'white--text subtitle-1', align:'center' },
        { text:'출원상태', value:'applicationStatus', sortable: false, class: 'white--text subtitle-1', width: "100", align:'center' },
        { text:'출원인이름', value:'applicantName', sortable: false, class: 'white--text subtitle-1', width: "120", align:'center' },
        { text:'대리인이름', value:'agentName', sortable: false, class: 'white--text subtitle-1', align:'center' },
        { text:'공고일자', value:'publicationDate', sortable: false, class: 'white--text subtitle-1', align:'center' },
        { text:'공고번호', value:'publicationNumber', sortable: false, class: 'white--text subtitle-1', align:'center' },
      ]
    }
  },
}
</script>

<style>
.table-title {
  color: rgb(255, 127, 165);
}

.result-image {
  height: auto;
  width: 200px;
}
.v-data-table tbody tr:hover:not(.v-data-table__expanded__content) {
  background: rgba(213,220,255,0.3) !important;
}
.v-data-table__wrapper {
  border-radius: 10px;
}
.v-pagination button:hover{
  background: rgba(130,177,255,0.3) !important;
}
.table-style span{
  font-family: 'Nanum Gothic', sans-serif;
}
.table-style thead{
  background-color: cornflowerblue;
}
.table-style th{
  border-right: solid white;
  font-family: 'Nanum Gothic', sans-serif;
}
.table-style th:last-child{
  border-right: none;
}
.table-style td {
  box-sizing: border-box;
  overflow: hidden;
  list-style: none;
  border-right: solid white;
  border-top: solid white;
}


</style>

