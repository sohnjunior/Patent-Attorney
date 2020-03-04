<template>
  <div>
    <NavBar></NavBar>
    
    <v-content>
      <v-container>
        <h1>조회 결과</h1>        
      </v-container>
      <PredictResult></PredictResult>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import PredictResult from '../components/PredictResult.vue';


export default {
  components: { NavBar, PredictResult },
}
</script>

<style>

</style>
