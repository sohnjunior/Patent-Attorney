<template>
    <v-container>
      <v-container>
        <vue2Dropzone id="dropzone"
          ref="fileUploadDropzone"
          :options="dropzoneOptions"
          :useCustomSlot="true"
          :duplicateCheck="true"
          @vdropzone-removed-file="fileRemoved"
          @vdropzone-duplicate-file="duplicateUpload"
          @vdropzone-max-files-exceeded="fileLimitExceeded"
          @vdropzone-file-added="fileAdded"
          @vdropzone-queue-complete="queueComplete">
          <div>
            <h3 class="dropzone-custom-title">Drag and drop</h3>
            <div class="subtitle">...or click here to select a file</div>
          </div>
        </vue2Dropzone>
      </v-container>

      <v-container fluid>
        <v-row justify="center">
          <Alerts :alertText="warningText" :showAlert="showAlert" @cancel="alertCancel"></Alerts>
        </v-row>
      </v-container>

      <v-container>
       <section>
          <div class="radio-box">
            <input type="radio" id="control_01" name="select" value="1" checked @click="toggleClicked(0)">
            <label for="control_01">
              <v-icon large>mdi-trademark</v-icon>
              <h4>상표 이미지</h4>
            </label>
          </div>
          <div class="radio-box">
            <input type="radio" id="control_02" name="select" value="2" @click="toggleClicked(1)">
            <label for="control_02">
              <v-icon large>mdi-desk</v-icon>
              <h4>디자인 이미지</h4>
            </label>
          </div>
        </section>
      </v-container>

      <v-container>
        <v-row justify="center">
          <div v-if="!submitFlag">
            <v-btn 
              class="white--text"
              :disabled="!uploadDone || !fileExist" 
              rounded 
              x-large 
              color="red lighten-3" 
              type="submit" 
              @click="submitFile" ><b>유사한 특허 확인하기</b></v-btn>
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
import Alerts from './Alerts.vue';
import { requestImagePrediction } from '../api/index';

export default {
  components: { vue2Dropzone, Alerts },
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
      },
      showAlert: false,
      warningText: '',
    }
  },
  computed: {
    fileExist() {
      if (this.inputFile.length == 0) {
        return false;
      } else {
        return true;
      }
    }
  },
  methods: {
    // dropzone 이벤트 관련 메소드
    fileAdded(file) {
      this.uploadDone = false;
      this.inputFile.push(file);
    },
    fileRemoved(file) {
      const idx = this.inputFile.indexOf(file);
      if(idx > -1) {
        this.inputFile.splice(idx, 1);
      }
    },
    queueComplete() {
      this.uploadDone = true;
    },
    fileLimitExceeded(file) {
      this.warningText = '최대 4개까지 추가할 수 있습니다';
      this.showAlert = true;
      this.$refs.fileUploadDropzone.removeFile(file);
    },
    duplicateUpload(file) {
      this.warningText = '중복된 파일이 존재합니다';
      this.showAlert = true;
      this.$refs.fileUploadDropzone.removeFile(file);
    },
    alertCancel() {
      this.uploadDone = true;
      this.showAlert = false;
    },
    toggleClicked(type) {
      this.toggled = type;
    },
    // 파일 업로드 관련 메소드
    settingStore(result) {
      this.$store.commit('setResultCount', { resultCount: result.request_num });
      this.$store.commit('setRequestImage', { imageData: result.request_image });
      this.$store.commit('setResultAppNum', { appNumbers: result.result_app_numbers });
    },
    async submitFile() {
      // spinner 작동
      this.submitFlag=true;

      const resultArray = [];
      for(let queryFile of this.inputFile) {
        let formData = new FormData();
        formData.append('file', queryFile);
        formData.append('selected', this.selected);
        formData.append('searchType', this.toggled);

        // 결과 이미지들 요청
        const { data } = await requestImagePrediction(formData);
        resultArray.push(JSON.parse(data));
      }

      // 파싱한 정보들을 store에 저장
      for(let result of resultArray) {
        this.settingStore(result);
      }

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

<style scoped lang="scss">
#dropzone {
  width: 65%;
  margin: 0 auto;
}
.dropzone-custom-title {
  margin-top: 0;
  color: #00b782;
}
.subtitle {
  color: #314b5f;
}

section {
  width: 30em;
  display: flex;
  margin: 0 auto;
}
section > div {
  flex: 0.5;
  padding: 1rem;
}
.radio-box {
  width: 600px;
}
input[type="radio"] {
  display: none;
  &:not(:disabled) ~ label {
    cursor: pointer;
  }
  &:disabled ~ label {
    color: hsla(150, 5%, 75%, 1);
    border-color: hsla(150, 5%, 75%, 1);
    box-shadow: none;
    cursor: not-allowed;
  }
}
label {
  height: 100%;
  display: block;
  color: #3f5566;
  background: white;
  border: 1px solid hsla(150, 75%, 50%, 1);
  border-radius: 20px;
  padding: 1.7rem;
  text-align: center;
  box-shadow: 0px 3px 10px -2px hsla(150, 5%, 65%, 0.5);
  position: relative;
}
input[type="radio"]:checked + label {
  background: hsla(150, 75%, 50%, 1);
  color: hsla(215, 0%, 100%, 1);
  box-shadow: 0px 0px 20px hsla(150, 100%, 50%, 0.75);
  
}

</style>
