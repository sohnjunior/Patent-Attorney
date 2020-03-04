import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function requestImagePrediction(formData) {
  return axios.post("/api/patent_image/predict/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}

function requestMarkInfo(appNum) {
  return axios.get("/api/patent_image/detail/", {
    params: {
      appnum: appNum
    }
  });
}

function requestDesignInfo() {
  return null;
}

export { requestImagePrediction, requestMarkInfo, requestDesignInfo }