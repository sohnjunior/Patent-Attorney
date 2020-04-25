import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { requestMarkInfo, requestDesignInfo } from '../api/index'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    requestImage: [], // 사용자가 요청한 이미지(base64)
    resultCount: [], // 사용자가 요청한 이미지 개수
    resultAppNumbers: [], // 결과 이미지들의 출원번호
    resultPatentInfos: [], // 결과 이미지들에 대한 특허 정보 
  },
  getters: {
    getResultCount: (state) => (idx) => {
      return state.resultCount[idx];
    },
    getAllRequestImage(state) {
      return state.requestImage;
    },
    getRequestImage: (state) => (idx) => {
      return state.requestImage[idx];
    },
    getPatentInfos: (state) => (idx) => {
      return state.resultPatentInfos[idx];
    }
  },
  mutations: {
    initData(state) {
      state.requestImage = [];
      state.resultCount = [];
      state.resultAppNumbers = [];
      state.resultPatentInfos = [];
    },
    setResultCount(state, payload) {
      state.resultCount.push(payload.resultCount);
    },
    setRequestImage(state, payload) {
      state.requestImage.push(payload.imageData);
    },
    setResultAppNum(state, payload) {
      state.resultAppNumbers.push(payload.appNumbers);
    },
    setResultPatentInfo(state, payload) {
      state.resultPatentInfos.push(payload.patentInfos);
    },
  },
  actions: {
    async getMarkInfo({ commit, state }) {
      for(let idx = 0; idx < state.requestImage.length; idx++) {
        var patentInfos = [];
        for (var appNum of state.resultAppNumbers[idx]) {
          const { data } = await requestMarkInfo(appNum);

          const result = JSON.parse(data);
          patentInfos.push(result);
        }

        commit('setResultPatentInfo', { patentInfos });
      }
    },
    async getDesignInfo({ commit, state }) {
      for(let idx = 0; idx < state.requestImage.length; idx++) {
        var patentInfos = [];
        for (var appNum of state.resultAppNumbers[idx]) {
          const { data } = await requestDesignInfo(appNum);

          const result = JSON.parse(data);
          patentInfos.push(result);
        }

        commit('setResultPatentInfo', { patentInfos });
      }
    },
  },
})
