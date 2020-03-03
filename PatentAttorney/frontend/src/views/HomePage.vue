<template>
  <div>
    <NavBar></NavBar>
    <InfoBox></InfoBox>
    <InputForm></InputForm>
    <Footer></Footer>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import InfoBox from '../components/InfoBox.vue';
import InputForm from '../components/InputForm.vue';
import Footer from '../components/Footer.vue';

export default {
  components: { NavBar, InfoBox, InputForm, Footer }
}
</script>

<style>

</style>