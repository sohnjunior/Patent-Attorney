<template>
  <div class="app">
    <v-container
    fill-height
    fluid
    grid-list-xl>
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        xs12
        md4
      >
        <v-card
          class="mx-auto"
          max-width="300px"
          >
            <v-img
              class="indigo--text align-end"
              height="auto"
              width="200px"
              :src="`data:image/jpeg;base64,${images[0]}`"></v-img>
             <hr/>
              <v-card-title>Request Image</v-card-title>
        </v-card>
      </v-flex>
      <v-flex
        xs12
        md8
      >
        <v-card>
          <v-card-title>
            Result
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="items"
            class="text-no-wrap"
            >
            <template
              slot="headerCell"
              slot-scope="{ headers }"
            >


            </template>
            <template v-slot:item.temp="{items}" >
              <td>
                 <img :src="`data:image/jpeg;base64,${images[1][0]}`" style="height:auto;width:200px">
              </td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </template>
          </v-data-table>
        </v-card>

      </v-flex>
    </v-layout>
  </v-container>
  </div>
</template>

<script>

export default {
  name: 'PredictResult',
  props:['images'],
  data(){
    return{
      headers:[
        { text:'Image',value:'temp'},
        { text:'상표명',value:'title'},
        { text:'출원인이름',value:'applicantName'},
        { text:'대리인이름',value:'agentName'},
        { text:'출원상태',value:'applicationStatus'},
        { text:'공고일자',value:'publicationDate'},
        { text:'공고번호',value:'publicationNumber'},
      ],
      items:[
        {
          temp:null,
          title:'s',
          applicantName:'a',
          agentName: 'm',
          applicationStatus:'p',
          publicationDate:'l',
          publicationNumber:'e'
        }
      ],
    }
  }
}
</script>

<style>

</style>
