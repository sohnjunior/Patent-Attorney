<template>
    <v-container>
      <v-container>
        <vue2Dropzone id="dropzone"
          ref="fileUploadDropzone"
          :options="dropzoneOptions"
          :useCustomSlot="true"
          :duplicateCheck="true"
          @vdropzone-duplicate-file="duplicateUpload"
          @vdropzone-max-files-exceeded="fileLimitExceeded"
          @vdropzone-file-added="fileAdded"
          @vdropzone-queue-complete="queueComplete">
          <div class="dropzone-custom-content">
            <h3 class="dropzone-custom-title">Drag and drop to upload content!</h3>
            <div class="subtitle">...or click to select a file from your computer</div>
          </div>
        </vue2Dropzone>
      </v-container>

      <v-container fluid class="py-2">
        <v-row justify="center">
          <div>
            <v-btn-toggle v-model="toggled">
              <v-btn>
                상표
              </v-btn>
              <v-btn>
                디자인
              </v-btn>
            </v-btn-toggle>
          </div>
        </v-row>
      </v-container>

      <v-container fluid class="py-2">
        <v-row justify="center">
          <div v-if="!submitFlag">
            <v-btn id="submit-button" :disabled="!uploadDone" outlined color="indigo" type="submit" @click="submitFile" >검색</v-btn>
          </div>
          <div v-else>
            <v-progress-circular indeterminate :rotate="20" :size="40" :width="5" color="light-blue"></v-progress-circular>
          </div>
        </v-row>
      </v-container>
    </v-container>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone';
import { requestImagePrediction } from '../api/index';

export default {
  components: { vue2Dropzone },
  data() {
    return {
      inputFile: [],
      submitFlag: false,
      selected: 10,
      toggled: 0,
      uploadDone: false,
      dropzoneOptions: {
        url: 'https://httpbin.org/post',
        maxFiles: 4,
        thumbnailWidth: 140,
        thumbnailMethod: 'contain',
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
    // dropzone 이벤트 관련 메소드
    fileAdded(file) {
      this.uploadDone = false;
      this.inputFile.push(file);
    },
    queueComplete() {
      this.uploadDone = true;
    },
    fileLimitExceeded(file) {
      alert('최대 4개까지 추가할 수 있습니다!');
      this.$refs.fileUploadDropzone.removeFile(file);
    },
    duplicateUpload(file) {
      alert('중복된 파일이 존재합니다!');
      this.$refs.fileUploadDropzone.removeFile(file);
    },

    // 파일 업로드 관련 메소드
    settingStore(result) {
      this.$store.commit('setResultCount', { resultCount: result.request_num });
      this.$store.commit('setRequestImage', { imageData: result.request_image });
      this.$store.commit('setResultImages', { imageData: result.images });
      this.$store.commit('setResultAppNum', { appNumbers: result.result_app_numbers });
    },
    async submitFile() {
      // check file existance
      if(!this.fileRegistered) {
        alert('파일을 선택해주세요');
        return;
      }

      // spinner 작동
      this.submitFlag=true;

      const resultArray = new Array();
      for(let queryFile of this.inputFile) {
        let formData = new FormData();
        formData.append('file', queryFile);
        formData.append('selected', this.selected);
        formData.append('searchType', this.toggled);

        // 결과 이미지들 요청
        const { data } = await requestImagePrediction(formData);
        resultArray.push(JSON.parse(data));
      }

      // TODO: 파싱한 정보들을 store에 저장 TODO 여러개 설정하도록
      console.log(resultArray);
      this.settingStore(resultArray[0]);
      
      // 결과 이미지들의 특허 정보 호출
      if(this.toggled === 0) {
        await this.$store.dispatch('getMarkInfo');
      } else {
        await this.$store.dispatch('getDesignInfo');
      }

      // 라우터로 predict 페이지로 이동
      this.$router.push({name: 'predict'});
      
    },
  }
}
</script>

<style scoped>
#dropzone {
  width: 65%;
  margin: 0 auto;
}
#submit-button {
  width: 5rem;
  height: 3rem;
}
</style>
