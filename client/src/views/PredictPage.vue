<template>
  <div>
    <NavBar></NavBar>

    <v-content class="py-0">
      <div class="result">
        <h1>Predict Result</h1>
      </div>
    </v-content>

    <v-content class="py-0">
      <v-container>
        <PredictResultWrapper></PredictResultWrapper>
      </v-container>
    </v-content>

    <Footer></Footer>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import PredictResultWrapper from '../components/PredictResultWrapper.vue';
import Footer from '../components/Footer.vue';

export default {
  components: { NavBar, PredictResultWrapper, Footer },
}
</script>

<style scoped>
hr {
  width: 80%;
  margin: 0 auto;
}

.result{
  text-align: center;
}
</style>
