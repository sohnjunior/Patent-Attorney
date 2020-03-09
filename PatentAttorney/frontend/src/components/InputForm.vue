<template>
  <div>
    <v-container>
      <vue2Dropzone id="dropzone" 
        :options="dropzoneOptions" 
        :useCustomSlot="true"
        @vdropzone-file-added="fileAdded">
        <div class="dropzone-custom-content">
          <h3 class="dropzone-custom-title">Drag and drop to upload content!</h3>
          <div class="subtitle">...or click to select a file from your computer</div>
        </div>
      </vue2Dropzone>
    </v-container>

    <v-container>
      <div id="select-count" class="submit-buttons">
        <v-select v-model="selected" :items="items" label="결과 이미지 개수" outlined></v-select>
      </div>
      
      <div class="submit-buttons" id="submit-button">
        <div v-if="!submit_flag">
          <v-btn class="ma-2" outlined color="indigo" type="submit" @click="submitFile" >결과 보기</v-btn>
        </div>
        <div v-else>
          <v-progress-circular indeterminate :rotate="20" :size="40" :width="5" color="light-blue"></v-progress-circular>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone';
import { requestImagePrediction } from '../api/index';

export default {
  components: { vue2Dropzone },
  data() {
    return {
      inputFile: null,
      selected: 5, // TODO
      submit_flag: false,
      items: [1, 2, 3, 4, 5], // TODO
      dropzoneOptions: {
        url: 'https://httpbin.org/post',
        maxFiles: 5,
        thumbnailWidth: 200,
        addRemoveLinks: true,
        dictRemoveFile: '파일 삭제',
        dictCancelUpload: '업로드 취소',
      }
    }
  },
  computed: {
    fileRegistered() {
      return (!this.inputFile ? false : true);
    }
  },
  methods: {
    fileAdded(file) {
      this.inputFile = file;
    },
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
        
        // 결과 이미지들의 특허 정보 호출
        this.$store.dispatch('getMarkInfo');

        // 라우터로 predict 페이지로 이동
        this.$router.push({name: 'predict'});
      } catch(error) {
        console.log('error : ', error);
      }
    },
  }
}
</script>

<style scoped>
#dropzone {
  width: 65%;
  margin: 0 auto;
}
.submit-buttons {
  margin: 0 auto;
}
#select-count {
  width: 10%;
}
#submit-button {
  width: 10%;
}
</style>