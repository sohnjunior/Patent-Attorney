<template>
  <v-container>
    <v-row justify="center">
      <span v-for="image in requestImages" :key="image">
        <v-img :src="`data:image/jpeg;base64,${image}`" class="preview-image"></v-img>
      </span>
    </v-row>
  </v-container>
</template>

<script>
export default {
  computed: {
    requestImages() {
      return this.$store.getters.getAllRequestImage;
    }
  }
}
</script>

<style scoped>
.preview-image {
  width: 80px;
  height: 80px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 3px;
  margin-left: 10px;
}
.preview-image:hover {
  box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}
</style>