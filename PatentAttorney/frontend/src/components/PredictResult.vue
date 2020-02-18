<template>
  <div class="app">
    <h1>결과사진</h1>
    <v-card class="d-inline-block mx-auto">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img :src="`data:image/jpeg;base64,${images[0][0]}`" width="300" height="auto"></v-img>

          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card class="d-inline-block mx-auto">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img :src="`data:image/jpeg;base64,${images[0][1]}`" width="300" height="auto"></v-img>
            
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card class="d-inline-block mx-auto">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img :src="`data:image/jpeg;base64,${images[0][2]}`" width="300" height="auto"></v-img>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card class="d-inline-block mx-auto">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img :src="`data:image/jpeg;base64,${images[0][3]}`" width="300" height="auto"></v-img>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card class="d-inline-block mx-auto">
      <v-container>
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img :src="`data:image/jpeg;base64,${images[0][4]}`" width="300" height="auto"></v-img>
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img{
  width:250px;
  height: auto;
}
</style>
