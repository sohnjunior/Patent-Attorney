<template>
  <div class="app">
    <h1>결과사진</h1>
    <img :src="`data:image/jpeg;base64,${images[0][0]}`">
    <img :src="`data:image/jpeg;base64,${images[0][1]}`">
    <img :src="`data:image/jpeg;base64,${images[0][2]}`">
    <img :src="`data:image/jpeg;base64,${images[0][3]}`">
    <img :src="`data:image/jpeg;base64,${images[0][4]}`">
  </div>
</template>

<script>

export default {
  name: 'PredictResult',
  props:['images'],
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
