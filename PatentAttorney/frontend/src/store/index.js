import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    requestImage: '', // 사용자가 요청한 이미지(base64)
    resultImages: [], // json으로 받은 결과 이미지들(base64)
    resultAppNumbers: [], // 결과 이미지들의 출원번호 
  },
  getters: {
    getRequestImage: state => {
      return state.requestImage;
    },
    getResultImages: state => {
      return state.resultImages;
    }
  },
  mutations: {
    setRequestImage(state, payload) {
      state.requestImage = payload.imageData;
    },
    setResultImages(state, payload) {
      state.resultImages = payload.imageData;
    },
    setResultAppNum(state, payload) {
      state.resultAppNumbers = payload.appNumbers;
    },
  },
})
