<template>
  <div class="App">
      <!--    받아온 이미지 데이터 출력하는 컴포넌트 -->
      <v-container fill-height color="black">
      <v-row align="start" class="white--text mx-auto" justify="center">
          <v-col class="white--text text-center" cols="12" tag="h1">
            <span class="font-weight-light">
              Result
            </span>
            <br>
          </v-col>
      </v-row>
      </v-container>
      <PredictResult v-bind:images="imageBytes"/>
  
  </div>
</template>

<script>
import PredictResult from '@/components/PredictResult.vue';


export default {
  components: { PredictResult },
}
</script>

<style>

</style>
