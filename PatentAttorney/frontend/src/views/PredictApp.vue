<template>
  <div class="App">
    <div v-if="!flag">

      <v-row
        align="center"
        class="black--text mx-auto"
        justify="center"
      >
          <v-col
            class="black--text text-center"
            cols="12"
            tag="h1"
          >
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


    <div class="py-3"/>
      <v-row>
        <v-col>
          <v-file-input v-model="file" label="Select Image File"  @change="handleFileUpload" outlined dense></v-file-input>
        </v-col>
        <v-col md="auto">
          <v-select
            :items="count"
            v-model="selected"
            label="Count"
            outlined
            @click="handleCountload">
          </v-select>
        </v-col>
        <v-col lg="2">
          <div v-if="!submit_flag">
            <v-btn class="ma-2" outlined color="indigo" type="submit" @click="submitFile" >제출</v-btn>
          </div>
          <div v-if="submit_flag">
            <v-progress-circular
              :indeterminate="indeterminate"
              :rotate="rotate"
              :size="size"
              :width="width"
              color="light-blue">
              {{ value }}
            </v-progress-circular>
          </div>
        </v-col>
      </v-row>
    </div>

    <!--    받아온 이미지 데이터 출력하는 컴포넌트 -->
    <div v-if="flag">
      <v-container fill-height color="black">
      <v-row
        align="start"
        class="white--text mx-auto"
        justify="center"
      >
          <v-col
            class="white--text text-center"
            cols="12"
            tag="h1"
          >
            <span class="font-weight-light">
              Result
            </span>
            <br>
          </v-col>
      </v-row>
      </v-container>
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
      submit_flag:false,
      count : [1,2,3,4,5],
      selected: 0,
      indeterminate:true,
      rotate:20,
      size:40,
    }
  },
  methods: {
    submitFile() {
      this.submit_flag=true;
      let formData = new FormData();

      formData.append('file', this.file);
      formData.append('selected', this.selected);

      axios.post("/api/patent_image/predict/", formData, {
        headers: {'Content-Type': 'multipart/form-data'}
      })
        .then((res) => {
          // 여기서 imageBytes에 json 파싱해서 images 값들 저장
          let result = jQuery.parseJSON(res.data);
          this.imageBytes.push(result.request_image);
          this.imageBytes.push(result.images);
          this.imageBytes.push(result.result_app_numbers);
          console.log(this.imageBytes[0]);
          console.log(this.imageBytes[1]);
          console.log(this.imageBytes[2]);
          // console.log(this.selected);
          // console.log(res);
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
      this.selected = this.$refs.count;
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
