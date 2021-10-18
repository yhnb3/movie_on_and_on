import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import infiniteScroll from "vue-infinite-scroll";
import router from "./router";
import store from "./store";
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueCookies from 'vue-cookies'


Vue.config.productionTip = false;
Vue.use(infiniteScroll);

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueCookies)

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount("#app");
