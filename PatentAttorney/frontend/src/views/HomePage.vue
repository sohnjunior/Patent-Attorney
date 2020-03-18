<template>
  <div>
    <NavBar></NavBar>
    <InfoBox></InfoBox>
    <FileUploadForm></FileUploadForm>
    <Footer></Footer>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import InfoBox from '../components/InfoBox.vue';
import FileUploadForm from '../components/FileUploadForm.vue';
import Footer from '../components/Footer.vue';

export default {
  components: { NavBar, InfoBox, FileUploadForm, Footer }
}
</script>

<style scoped>

</style>
