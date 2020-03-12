<template>
  <div>
    <NavBar></NavBar>
    
      <v-content>
        <v-container>
          <h1>조회 결과</h1>  
        </v-container> 
        <hr>
        <v-container>
          <PredictResult></PredictResult>
        </v-container>
      </v-content>
      
    <Footer></Footer>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import PredictResult from '../components/PredictResult.vue';
import Footer from '../components/Footer.vue';

export default {
  components: { NavBar, PredictResult, Footer },
}
</script>

<style scoped>
hr {
  width: 80%;
  margin: 0 auto;
}
</style>
