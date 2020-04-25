<template>
  <div class="top">
    <v-content>
      <v-container class="fill-height">
          <div class="text">
          <v-row class="white--text mx-auto" align="start">
            <v-col class="white--text text-center" cols="12" tag="h1">
              <span style="color: rgb(250, 245, 245)">
                <h1>특허 유사도 분석 서비스</h1>
              </span>
              <br>
              <span>
                <h4 class="font-weight-thin">BY PANG'S</h4>
              </span>
              <br>
              <p class="font-weight-thin" id="explain">
                Patent Image similarity analysis service
                <br>
                using deep-ranking algorithm
              </p>
            </v-col>
          </v-row>
          </div>
      </v-container>
    </v-content>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
#explain {
  animation: fadein 2s;
}

@keyframes fadein {
  from { opacity: 0; transform: translateY(2em) }
  to { opacity: 1; transform: translateY(0em) }
}

.text{
  width: 100%;
  height: 100%;
  text-align: center;
  align-items: center;
  justify-content: center;
}
.top{
  padding-top: 100px;
}
</style>
