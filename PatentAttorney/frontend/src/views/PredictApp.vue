<template>
  <div class="App">
    <div v-if="!flag">
      <input type="file" id="file" name="file" ref="file" @change="handleFileUpload">
      <button type="submit" @click="submitFile">제출</button>
    </div>
        <hr>
        <!--    받아온 이미지 데이터 출력하는 부분 - 수정 필요 -->
    <div v-if="flag">
      <PredictResult v-bind:images = "imageBytes"/>
    </div>
  </div>
</template>

<script>
import PredictResult from "@/components/PredictResult.vue";
import axios from 'axios'
import jQuery from 'jquery'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  name: 'PredictApp',
  components: {
    PredictResult
  },
  data() {
    return {
      file: '',
      imageBytes: [], // json으로 받은 이미지 raw 데이터를 저장하는 배열
      flag: false
    }
  },
  methods: {
    submitFile() {
      let formData = new FormData();
      formData.append('file', this.file);

      axios.post("/api/patent_image/predict/", formData, {
        headers: {'Content-Type': 'multipart/form-data'}
      })
        .then((res) => {
          // 여기서 imageBytes에 json 파싱해서 images 값들 저장해야
          var result = jQuery.parseJSON(res.data);
          this.imageBytes.push(result.images);
          console.log(this.imageBytes[0][0]);
          console.log(res);
          this.flag = true;
        })
        .catch((err) => {
          console.log('[ERROR]', err);
        });
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    }
  }
}

</script>

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
