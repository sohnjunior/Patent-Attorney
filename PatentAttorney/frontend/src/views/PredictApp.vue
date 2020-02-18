<template>
  <div class="App">
    <div v-if="!flag">
      <v-row>
        <v-col cols="15" md="10">
          <v-file-input v-model="file" label="Select Image File"  @change="handleFileUpload" outlined dense></v-file-input>
        </v-col>
        <v-col cols="15" md="10">
          <v-select v-model="count" :items="count" label="Count" required @change="handleCountload"></v-select>
        </v-col>
        <v-col cols="15" md="10">
          <v-btn class="ma-2" outlined color="indigo" type="submit" @click="submitFile">제출</v-btn>
        </v-col>
      </v-row>
    </div>
        <hr>
        <!--    받아온 이미지 데이터 출력하는 부분 - 수정 필요 -->
    <div v-if="flag">
      <PredictResult v-bind:images="imageBytes"/>
    </div>
  </div>
</template>

<script>
import PredictResult from "@/components/PredictResult.vue"
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
      flag: false,
      count : [1,2,3,4,5,],
    }
  },
  methods: {
    submitFile() {
      let formData = new FormData();
      formData.append('file', this.file);
      formData.append('count', this.count);

      axios.post("/api/patent_image/predict/", formData, {
        headers: {'Content-Type': 'multipart/form-data'}
      })
        .then((res) => {
          // 여기서 imageBytes에 json 파싱해서 images 값들 저장
          let result = jQuery.parseJSON(res.data);
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
    },
    handleCountload() {
      this.count = this.$refs.count;
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
  .v-file-input{
   length: 200;
  }
</style>
