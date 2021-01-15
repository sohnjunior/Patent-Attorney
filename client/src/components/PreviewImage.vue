<template>
  <v-container>
    <v-row justify="center">
      <span @click="prevImage" class="left-button"> <font-awesome-icon :icon="['fas', 'angle-left']" size="3x"/> </span>
      <span v-for="(image, index) in requestImages" :key="image">
        <v-img :src="`data:image/jpeg;base64,${image}`" :class="imageStyle(index)"></v-img>
      </span>
      <span @click="nextImage" class="right-button"> <font-awesome-icon :icon="['fas', 'angle-right']" size="3x"/> </span>
    </v-row>
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
  width: 60px;
  height: 60px;
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
.left-button {
  cursor: pointer;
  margin-top: 15px;
  margin-right: 30px;
  color:rgba(0, 139, 186, 0.342);
}
.right-button {
  cursor: pointer;
  margin-top: 15px;
  margin-left: 30px;
  color:rgba(0, 139, 186, 0.342);
}
</style>