const API_BASE_URL = 'http://127.0.0.1:8003/';
// const API_BASE_URL =  'https://65wc0j31f7.execute-api.us-east-1.amazonaws.com/prod/';

export const API_ENDPOINTS = {
    POST_LOGIN: API_BASE_URL + 'users/login/',
    POST_SIGNUP: API_BASE_URL + 'users/signup/',
    GET_CLUSTERS: `${API_BASE_URL}clusters/:userId`,
    POST_SCHEDULER: `${API_BASE_URL}scheduler/:userId`,
    POST_CREATE_USER: API_BASE_URL + 'users/',
    GET_USER: `${API_BASE_URL}users/:userId`,
    DELETE_USER: `${API_BASE_URL}users/:userId`,
    POST_CREATE_CONV: API_BASE_URL + 'conversations/',
    GET_CONV: `${API_BASE_URL}conversations/:convId`,
    GET_ALL_CONV: API_BASE_URL + 'conversations/',
    PUT_UPDATE_CONV: `${API_BASE_URL}conversations/:convId`,
    DELETE_CONV: `${API_BASE_URL}conversations/:convId`,
    POST_UPLOAD_DOCS: `${API_BASE_URL}upload/:userId`
};