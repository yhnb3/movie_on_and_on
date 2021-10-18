<template>
  <v-app id="app">
    <!-- <toolbar /> -->
    <drawer />
    <route-view />
    <go-top />
  </v-app>
</template>

<script>
import Drawer from "@/components/Drawer";
import Toolbar from "@/components/Toolbar";
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default {
  components: {
    Drawer,
    Toolbar,
    RouteView,
    GoTop,
  },
  created() {
    this.$store.commit('checkToken',this.$cookies.get('auth-token'))
    this.$store.commit('checklogin',this.$cookies.isKey('auth-token')) 
  },
  methods: {
  }

};
</script>

<style>

.containerapp {
  margin-top: 50px;
}

</style>