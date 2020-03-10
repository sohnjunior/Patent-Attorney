<template>
  <div>
    <v-content>
      <v-container class="fill-height" fluid>
        <div class="img-wrap">
          <div class="text">
          <v-row class="black--text mx-auto" :align="start">
            <v-col class="black--text text-center" cols="12" tag="h1">
              <span class="font-weight-black">
                ImagePredict Service
              </span>
              <br>
              <span class="font-weight-light">
                BY PANG'S
              </span>
              <br>
              <span class="font-weight-light">
                이미지 덧댈 예정
              </span>
              <br>
            </v-col>
          </v-row>
          </div>
          <v-img class="blur" src="../assets/background.jpg"/>
        </div>
      </v-container>
    </v-content>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.img-wrap{
  width:80%;
  height: 80%;
  align-items: center;
  justify-content: center;
  position:relative;
}
.blur{
  filter:brightness(70%);
  z-index: 1;
}
.text{
  position: absolute;
  width: 100%;
  height: 100%;
  font-size: 20px;
  color: #FFFFFF;
  font-weight: 600;
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
</style>