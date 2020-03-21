<template>
  <v-container>
    <v-row justify="center">
      <span v-for="(image, index) in requestImages" :key="image">
        <v-img :src="`data:image/jpeg;base64,${image}`" :class="imageStyle(index)"></v-img>
      </span>
    </v-row>
    <button @click="prevImage"> 이전 </button>
    <button @click="nextImage"> 다음 </button>
  </v-container>
</template>

<script>
import { EventBus } from '../utils/event_bus.js';

export default {
  data() {
    return {
      selected: 0  // 현재 선택된 프리뷰 이미지
    }
  },
  computed: {
    requestImages() {
      return this.$store.getters.getAllRequestImage;
    },
  },
  methods: {
    imageStyle(index) {
      return {
        'preview-image': this.selected !== index,
        'preview-image-selected': this.selected === index,
      }
    },
    prevImage() {
      if(this.selected > 0) {
        this.selected -= 1;
        EventBus.$emit('index-change', this.selected);
      }
    },
    nextImage() {
      if(this.selected < this.requestImages.length - 1) {
        this.selected += 1;
        EventBus.$emit('index-change', this.selected);
      }
    }
  }
}
</script>

<style scoped>
.preview-image {
  width: 65px;
  height: 65px;
  opacity: 0.5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 3px;
  margin-left: 10px;
  transition-property: width, height, opacity;
  transition-duration: 0.4s;
  transition-timing-function: ease;
}
.preview-image-selected {
  width: 80px;
  height: 80px;
  opacity: 1.0;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 3px;
  margin-left: 10px;
  box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
}
</style>