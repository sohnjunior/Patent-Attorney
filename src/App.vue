<template>
  <v-app>
    <div class="bg-back">
        <div class="bg-size rearrange"></div>
        <div class="bg-size rearrange"></div>
    </div>
    <div class="bg bg-size arrange">
        <div class="rearrange">
            <div class="line arrange">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    <div class="view">
      <router-view></router-view>
    </div>
  </v-app>
</template>

<script>

</script>

<style scoped>
.bg-size{
  min-height: 670px;
  padding: 0 0;
  overflow: hidden;
  margin-bottom: 0px;
}
.bg-back{
  position: relative;
}
.bg-back div{
  background: linear-gradient(90deg, rgba(31,90,175,0.2), rgba(24,126,171,0.2), rgba(18,16,217,0.2));
  position: absolute;
  width: 100%;
  margin-top: 10px;
}
.bg-back :first-child{
  transform-origin: bottom;
  transform: skewY(-8deg);
}
.bg-back :last-child{
  transform-origin: right;
  transform: skewY(5deg);
  max-width: 100%;
}
.bg{
  background:linear-gradient(90deg, rgba(99,251,249,1) 0%, rgba(59,145,254,1) 50%, rgba(60,26,173,1) 100%);
  position: relative;
}
.arrange {
  transform: skewY(-11deg);
  transform-origin: 0;
}
.rearrange{
  transform: skewY(11deg);
  transform-origin: 0;
}
.line span{
  border-radius: 500px;
  position: absolute;
}
.line :first-child{
  width: 37%;
  height: 75px;
  top: 25px;
  left: 17%;
  background-image: linear-gradient(90deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0));
}
.line :nth-child(2){
  width: 70%;
  height: 85px;
  top: -30px;
  left: 33%;
  background: #6481df;
}
.line :nth-child(3){
  width: 33%;
  height: 10px;
  top: 180px;
  left: 70%;
  background: linear-gradient(90deg, #ffffff2b, #ffffff00);
}
.line :nth-child(4){
  width: 10px;
  height: 10px;
  top: 180px;
  left: 68%;
  background-color: rgba(255, 255, 255, 0.17);
}
.line :nth-child(5){
  width: 70%;
  height: 85px;
  top: 300px;
  left: 55%;
  background: #3c1aad3f;
}
.line :nth-child(6){
  width: 47%;
  height: 85px;
  top: 400px;
  left: -100px;
  background: linear-gradient(90deg, #00abfa, #0b07e400);
}
.line :nth-child(7){
  width: 20%;
  height: 10px;
  top: 520px;
  left: 4%;
  background: linear-gradient(90deg, #ffffff14, #ffffff00);
}
.line :nth-child(8){
  width: 10px;
  height: 10px;
  top: 520px;
  left: 2%;
  background: #ffffff14;
}
.view{
  position: absolute;
  width: 1519px;
}
</style>
