import Vue from "vue";
import Vuex from "vuex";
import data from "./modules/data";
import app from "./modules/app";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    data,
    app
  },
  state: {
    base_url: 'https://j3d204.p.ssafy.io/back',
    token: null,
    islogin: false,
    updatebox: null
  },
  mutations: {
    checkToken: function(state, token) {
      state.token = token;
    },
    checklogin: function(state, flag){
      state.islogin = flag;
    },
    updateinfo: function(state, box){
      state.updatebox = box
    }
  }
});
