import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function requestImagePrediction(formData) {
  return axios.post("/api/patent/predict/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}

function requestMarkInfo(appNum) {
  return axios.get("/api/mark/detail", {
    params: {
      appnum: appNum
    }
  });
}

function requestDesignInfo(appNum) {
  return axios.get("api/design/detail", {
    params: {
      appnum: appNum
    }
  });
}

export { requestImagePrediction, requestMarkInfo, requestDesignInfo }