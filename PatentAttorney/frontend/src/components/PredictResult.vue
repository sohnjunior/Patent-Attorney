<template>
  <div class="app">
    <h1>유사도 측정 결과</h1>

    <v-card v-for="image in images[0]" class="d-inline-block mx-auto" v-bind:key="image">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img :src="`data:image/jpeg;base64,${image}`" width="300" height="auto"></v-img>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

  </div>
</template>

<script>
export default {
  name: 'PredictResult',
  props:['images'],
}
</script>

<style>

</style>
