<template>
  <v-card class="mx-auto" max-width="200px">
    <v-img :src="`data:image/jpeg;base64,${requestImage(0)}`" class="request-image"></v-img>
  </v-card>
</template>

<script>
export default {
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