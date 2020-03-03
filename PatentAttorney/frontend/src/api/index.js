import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function requestImagePrediction(formData) {
  axios.post("/api/patent_image/predict/", formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}

export { requestImagePrediction }