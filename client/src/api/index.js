import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://ec2-15-164-228-101.ap-northeast-2.compute.amazonaws.com/',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
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
  return instance.get(`/api/design/detail/${appNum}/`);
}

export { requestImagePrediction, requestMarkInfo, requestDesignInfo }