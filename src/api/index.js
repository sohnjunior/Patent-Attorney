import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/'
});

function requestImagePrediction(formData) {
  return instance.post("/api/patent/predict/", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}

function requestMarkInfo(appNum) {
  return instance.get(`/api/mark/detail/${appNum}/`);
}

function requestDesignInfo(appNum) {
  return instance.get(`/api/mark/detail/${appNum}/`);
}

export { requestImagePrediction, requestMarkInfo, requestDesignInfo }