<template>
  <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    dark
    floating
    persistent
    mobile-break-point="500"
    width="220"
  >
    <v-layout column>
      <v-list rounded>
          <v-list-item
            v-for="(link, i) in links"
            :key="i"
            :to="link.to"
            active-class="blue lighten-1 white--text"
            class="v-list-item ma-3"
          >
            <v-list-item-action>
              <v-icon>{{ link.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-title v-text="link.text" />
          </v-list-item>
        <span v-if="this.$store.state.islogin">
          <v-list-item
            @click="logout()"
            active-class="blue lighten-1 white--text"
            class="v-list-item ma-3"
          >
            <v-list-item-action>
              <v-icon>{{ "mdi-home" }}</v-icon>
            </v-list-item-action>
            <v-list-item-title v-text="'Logout'" />
          </v-list-item>
        </span>
        <span v-else>
          <v-list-item
            v-for="(link, i) in linkslogin"
            :key="i"
            :to="link.to"
            active-class="blue lighten-1 white--text"
            class="v-list-item ma-3"
          >
            <v-list-item-action>
              <v-icon>{{ link.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-title v-text="link.text" />
          </v-list-item>
        </span>
      </v-list>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  props: {
    opened: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    links: [
      {
        to: "/",
        icon: "mdi-home",
        text: "Home"
      },
      {
        to: "/search",
        icon: "mdi-movie",
        text: "Movie"
      },
       {
        to: "/list",
        icon: "fa-bullhorn",
        text: "Community"
      },
      {
        to: "/form",
        icon: "fa-bullhor",
        text: "Write"
      } 
    ],
    linkslogin: [
            {
        to: "/login",
        icon: "fa-bullhorn",
        text: "Login"
      },
      {   
        to: "/signup",
        icon: "fa-bullhorn",
        text: "Signup"
      }, 
    ]
  }),
  computed: {
    ...mapState("app", ["drawer"]),
    inputValue: {
      get() {
        return this.drawer;
      },
      set(val) {
        this.setDrawer(val);
      }
    }
  },

  methods: {
    ...mapMutations("app", ["setDrawer"]),
    movepage(path){
      this.$router.push(path)
    },
    logout(){
      this.$cookies.remove('auth-token')
      this.$cookies.remove('userid')
      alert('로그아웃 되었습니다.')
      this.$store.commit('checkToken',this.$cookies.get('auth-token'))
      this.$store.commit('checklogin',this.$cookies.isKey('auth-token'))
    }
  }
};
</script>
