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
          @vdropzone-file-added="fileAdded">
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
          <div v-if="!submit_flag">
            <v-btn id="submit-button" outlined color="indigo" type="submit" @click="submitFile" >검색</v-btn>
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
      inputFile: null,
      submit_flag: false,
      selected: 10,
      toggled: 0,
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
      this.inputFile = file;
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
    async submitFile() {
      // check file existance
      if(!this.fileRegistered) {
        alert('파일을 선택해주세요');
        return;
      }

      let formData = new FormData();
      formData.append('file', this.inputFile);
      formData.append('selected', this.selected);
      formData.append('searchType', this.toggled);

      try {
        this.submit_flag=true;

        // 결과 이미지들 요청
        const response = await requestImagePrediction(formData);

        // JSON 파싱한 후 필요한 정보들 store에 저장
        const result = JSON.parse(response.data);
        this.$store.commit('setResultCount', { resultCount: result.request_num });
        this.$store.commit('setRequestImage', { imageData: result.request_image });
        this.$store.commit('setResultImages', { imageData: result.images });
        this.$store.commit('setResultAppNum', { appNumbers: result.result_app_numbers });

        // 결과 이미지들의 특허 정보 호출
        if(this.toggled === 0) {
          await this.$store.dispatch('getMarkInfo');
        } else {
          await this.$store.dispatch('getDesignInfo');
        }

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
#submit-button {
  width: 5rem;
  height: 3rem;
}
</style>
