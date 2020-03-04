<template>
  <div>
    <v-row>
      <v-col>
        <v-file-input v-model="inputFile" label="요청 이미지 선택" outlined dense></v-file-input>
      </v-col>
      <v-col>
        <v-select v-model="selected" :items="items" label="결과 이미지 개수" outlined></v-select>
      </v-col>
      <v-col>
        <div v-if="!submit_flag">
          <v-btn class="ma-2" outlined color="indigo" type="submit" @click="submitFile" >결과 보기</v-btn>
        </div>
        <div v-else>
          <v-progress-circular indeterminate :rotate="20" :size="40" :width="5" color="light-blue"></v-progress-circular>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { requestImagePrediction } from '../api/index';

export default {
  data() {
    return {
      inputFile: null,
      selected: 5, // TODO
      submit_flag: false,
      items: [1, 2, 3, 4, 5], // TODO
    }
  },
  computed: {
    fileRegistered() {
      return (!this.inputFile ? false : true);
    }
  },
  methods: {
    async submitFile() {
      // check file existance
      if(!this.fileRegistered) {
        alert('파일을 선택해주세요');
        return;
      }
      
      let formData = new FormData();
      formData.append('file', this.inputFile);
      formData.append('selected', this.selected);
      
      try {
        this.submit_flag=true;

        // 결과 이미지들 요청
        const response = await requestImagePrediction(formData);
        
        // JSON 파싱한 후 필요한 정보들 store에 저장
        const result = JSON.parse(response.data);
        this.$store.commit('setRequestImage', { imageData: result.request_image });
        this.$store.commit('setResultImages', { imageData: result.images });
        this.$store.commit('setResultAppNum', { appNumbers: result.result_app_numbers });
        
        // 라우터로 predict 페이지로 이동
        this.$router.push({name: 'predict'});
      } catch(error) {
        console.log('error : ', error);
      }
    },
  }
}
</script>

<style>

</style>