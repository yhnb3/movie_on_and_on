<template>

<div  style="height: 100vh;
    background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
    overflow: hidden;
    filter: drop-shadow(0 0 10px white);">




<div class="container">

  <!-- <h1><img src="../assets/img/logo.PNG" alt=""></h1> -->
  <div
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="10"
  >
    <v-container fill-height fluid grid-list-xl>
      <v-layout justify-center wrap mt-5>
        <v-flex xs12 md8>
          <card title="🎥 SEARCH MOVIE">
            <v-form>
              <v-container py-0>
                <v-layout wrap>
                    <b-form-radio-group id="radio-group-2" v-model="selected" name="radio-sub-component">
                      <b-form-radio value="title">Movie</b-form-radio>
                      <b-form-radio value="actor">Actor</b-form-radio>
                      <b-form-radio value="director">Director</b-form-radio>
                    </b-form-radio-group>
                  <v-flex xs12 md12>
                    <v-text-field v-model="storeName" label="내용을 입력해주세요" />
                  </v-flex>
                  <v-flex xs12 text-center>
                    <v-btn
                      large
                      class="indigo white--text ma-5"
                      rounded
                      color="white lighten-1"
                      @click="Goresult"
                    >SEARCH</v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </card>
          <v-divider class="mx-4" />
        </v-flex>

        <v-flex xs12 md8>
          <v-flex v-for="store in stores" :key="store.id" pa-4>
            <store-list-card
              :id="store.id"
              :name="store.name"
              :categories="store.categories"
              :address="store.address"
              :tel="store.tel"
            />
          </v-flex>
        </v-flex>
      </v-layout>
    </v-container>
  </div>

</div>
</div>


</template>

<script>
import Card from "@/components/Card";
import StoreListCard from "@/components/StoreListCard";
import { mapState, mapActions } from "vuex";
export default {
  components: {
    Card,
    StoreListCard
  },
  data: () => ({
    storeName: "",
    loading: true,
    selected: null,
  }),
  computed: {
    ...mapState({
      stores: state => state.data.storeSearchList,
      page: state => state.data.storeSearchPage
    })
  },
  methods: {
    ...mapActions("data", ["getStores"]),
    onSubmit: async function() {
      const params = {
        name: this.storeName,
        page: 1,
        append: false
      };
      await this.getStores(params);
      this.loading = false;
    },
    loadMore: async function() {
      this.loading = true;
      const params = {
        name: this.storeName,
        page: this.page,
        append: true
      };
      await this.getStores(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    Goresult() {
      this.$router.push('/searchlist/'+this.storeName+'/'+this.selected)
    }
  }
};
</script>

<style>
@font-face { font-family: 'TmoneyRoundWindExtraBold'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-07@1.0/TmoneyRoundWindExtraBold.woff') format('woff'); font-weight: normal; font-style: normal; }
* {
  font-family: 'TmoneyRoundWindExtraBold';
}

.headline {
  font-family: 'TmoneyRoundWindExtraBold';
  color: black;
  font-size: 30pt;

}


</style>