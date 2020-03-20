<template>
  <v-container>
    <v-row>
      <v-card class="mx-auto" max-width="200px">
        <v-img :src="`data:image/jpeg;base64,${requestImage(0)}`" class="request-image"></v-img>
      </v-card>
    </v-row>
    <br>
    <v-row>
      <PreviewImage></PreviewImage>
    </v-row>
  </v-container>
</template>

<script>
import PreviewImage from './PreviewImage.vue';

export default {
  components: { PreviewImage },
  computed: {
    requestImage() {
      return (idx) => {
        return this.$store.getters.getRequestImage(idx);
      }
    },
  }
}
</script>

<style scoped>
.request-image {
  width: 200px;
  height: auto;
}
</style>