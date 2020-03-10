import Vue from 'vue'
import Vuex from 'vuex'
import { requestMarkInfo, requestDesignInfo } from '../api/index';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    requestImage: '', // 사용자가 요청한 이미지(base64)
    resultCount: 0, // 사용자가 요청한 이미지 개수
    resultImages: [], // json으로 받은 결과 이미지들(base64)
    resultAppNumbers: [], // 결과 이미지들의 출원번호
    resultPatentInfos: [], // 결과 이미지들에 대한 특허 정보 
  },
  getters: {
    getResultCount: state => {
      return state.resultCount;
    },
    getRequestImage: state => {
      return state.requestImage;
    },
    getResultImages: state => {
      return state.resultImages;
    },
    getPatentInfos: state => {
      return state.resultPatentInfos;
    }
  },
  mutations: {
    setResultCount(state, payload) {
      state.resultCount = payload.resultCount;
    },
    setRequestImage(state, payload) {
      state.requestImage = payload.imageData;
    },
    setResultImages(state, payload) {
      state.resultImages = payload.imageData;
    },
    setResultAppNum(state, payload) {
      state.resultAppNumbers = payload.appNumbers;
    },
    setResultPatentInfo(state, payload) {
      state.resultPatentInfos = payload.patentInfos;
    },
  },
  actions: {
    async getMarkInfo({ commit, state }) {
      var patentInfos = new Array();
      for(var appNum of state.resultAppNumbers) {
        const response = await requestMarkInfo(appNum);

        const result = JSON.parse(response.data);
        patentInfos.push(result);
      }

      commit('setResultPatentInfo', { patentInfos });
    },
    async getDesignInfo({ commit, state }) {
      var patentInfos = new Array();
      for (var appNum of state.resultAppNumbers) {
        const response = await requestDesignInfo(appNum);

        const result = JSON.parse(response.data);
        patentInfos.push(result);
      }

      commit('setResultPatentInfo', { patentInfos });
    },
  },
})
