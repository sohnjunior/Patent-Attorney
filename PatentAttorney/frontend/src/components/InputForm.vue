<template>
  <div>
    <v-row>
      <v-col>
        <v-file-input v-model="file" label="Select Image File"  @change="handleFileUpload" outlined dense></v-file-input>
      </v-col>
      <v-col md="auto">
        <v-select :items="count" v-model="selected" label="Count" outlined @click="handleCountload"></v-select>
      </v-col>
      <v-col lg="2">
        <div v-if="!submit_flag">
          <v-btn class="ma-2" outlined color="indigo" type="submit" @click="submitFile" >제출</v-btn>
        </div>
        <div v-else>
          <v-progress-circular indeterminate :rotate="20" :size="40" :width="width" color="light-blue">
            {{ value }}
          </v-progress-circular>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { requestImagePrediction } from '../api/index';

import jQuery from 'jquery';

export default {
  data() {
    return {
      file: '',
      imageBytes: [], // json으로 받은 이미지 raw 데이터를 저장하는 배열
      submit_flag: false,
      count: [1,2,3,4,5],
      selected: 0,
    }
  },
  methods: {
    async submitFile() {
      let formData = new FormData();
      formData.append('file', this.file);
      formData.append('selected', this.selected);

      try {
        this.submit_flag=true;
        const response = await requestImagePrediction(formData);
        
        // 여기서 imageBytes에 json 파싱해서 images 값들 저장
        let result = jQuery.parseJSON(response.data);
        this.imageBytes.push(result.request_image);
        this.imageBytes.push(result.images);
        this.imageBytes.push(result.result_app_numbers);

        this.$route.push({name: 'predict'});
      } catch(error) {
        console.log('error : ', error);
      }
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

<style>

</style>