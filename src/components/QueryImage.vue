<template>
  <v-container>
    <v-row>
      <v-card class="mx-auto" max-width="200px">
        <v-img :src="`data:image/jpeg;base64,${requestImage(imageIdx)}`" class="request-image"></v-img>
      </v-card>
    </v-row>
    <br>
    <v-row>
      <PreviewImage></PreviewImage>
    </v-row>
  </v-container>
</template>

<script>
import { EventBus } from '../utils/event_bus.js';
import PreviewImage from './PreviewImage.vue';

export default {
  components: { PreviewImage },
  data() {
    return {
      imageIdx: 0
    }
  },
  computed: {
    requestImage() {
      return (idx) => {
        return this.$store.getters.getRequestImage(idx);
      }
    },
  },
  created() {
    EventBus.$on('index-change', (idx) => {
      this.imageIdx = idx;
    });
  }
}
</script>

<style scoped>
.request-image {
  width: 200px;
  height: auto;
}
</style>