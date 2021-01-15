<template>
  <div>
    <NavBar></NavBar>
    <FileUploadForm></FileUploadForm>
    <Footer></Footer>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import FileUploadForm from '../components/FileUploadForm.vue';
import Footer from '../components/Footer.vue';

export default {
  components: { NavBar, FileUploadForm, Footer }
}
</script>

<style scoped>

</style>
