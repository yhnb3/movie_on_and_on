<template>
  <div class="container" style="margin-top:50px;">

      <!-- <h1><img src="../assets/img/logo.PNG" alt=""></h1> -->
    <h1 style="margin-left: 250px;">🏆 당신이 좋아할만한 영화예요! 🏆</h1>
    <div v-if="this.$store.state.islogin">
    <div style="margin-left:350px;">
      <v-btn rounded color="primary" style="margin-left:50px" @click="train">평가 반영하기</v-btn>
      <v-btn rounded color="primary" style="margin-left:50px" @click="recom">새로 추천받기</v-btn>
    </div>

    <div v-if="moviedata.length == 0">
      <div class="carousel-3d-container" style="border: 20px solid #343a40; background-color: #343a40; height: 550px !important; margin:20px auto">
        <div class="square">
          <div class="spin"></div>
        </div>
        <p style="margin-left:280px; margin-top:25px; font-size:3rem; color:white">로딩 중 입니다.</p>
      </div>
    </div>
    <div v-else id="carousel">
      <carousel-3d class="carousel-3d-container" style="border: 20px solid #343a40; background-color: #343a40; height: 550px !important; margin">
        <span v-for="(item,n) in moviedata" :key="n">
          <slide :index = "n">
              <div>
                <h2><strong>{{item.title}}</strong></h2>
              </div>
              <div>
                <img style="height:500px; width: 360px" :src="'http://image.tmdb.org/t/p/w200'+item.poster_path"/>
              </div>
          </slide>
        </span>
      </carousel-3d>
    </div>
    <!-- 등급 가이드 -->
    <div class="container grade-guide">
      <!-- <img :src="require('../../assets/img/lv'+level(user.grade)+'.png')" style="width: 100px; display: inline-block;" /> -->
    </div>
    </div>
    <div v-else>
      <div class="carousel-3d-container" style="border: 20px solid #343a40; background-color: #343a40; height: 550px !important; margin:20px auto">
        <p style="margin-left:250px; margin-top:150px; font-size:3rem; color:white">회원가입 하시고</p>
        <p style="margin-left:180px; font-size:3rem; color:white">추천 영화를 확인하세요!</p>
      </div>
    </div>
  </div>  


  
</template>

<script>
import axios from 'axios'
  import {Carousel3d, Slide}  from 'vue-carousel-3d'

export default {
    name: 'Record',
    components: {
      Carousel3d,
      Slide
    },
  data(){
    return {
        user : {'grade':null},
        boundary : [
          '0 ~ 99 점',
          '100 ~ 199 점',
          '200 ~ 299 점',
          '300 ~ 399 점',
          '400 ~ 499 점',
          '500 ~ 599 점',
          '600 점 이상',
          '700 점 이상',
          '800 점 이상',
          '900 점 이상'
          ],
        line : [0,100,200,300,400,500,600,700,800,900],
        moviedata : [],
        rating : 10
    }
  },
  methods: {
    // 기존에 있던 코드
    train() {
      this.moviedata = []
      axios.get(this.$store.state.base_url +'/movie/train/')
      .then((response) => {
        this.recom()
      })
      .catch((error) => {
        console.log(error)
      })
    },
    recom() {
      this.moviedata = []
      axios.get(this.$store.state.base_url +'/movie/recommend/all',{
        headers : {'Authorization' : 'jwt '+this.$cookies.get('auth-token')}
      })
      .then((response) => {
        this.moviedata = response.data
      })
      .catch((error) => {
        console.log(error)
      })
    }
  },
  created() {
    this.recom()
  }
}
</script>


<style scoped>

@import url(https://fonts.googleapis.com/css?family=Vollkorn:bold);


@font-face { font-family: 'TmoneyRoundWindExtraBold'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-07@1.0/TmoneyRoundWindExtraBold.woff') format('woff'); font-weight: normal; font-style: normal; }

* {
  font-family: 'TmoneyRoundWindExtraBold';
}

  body {
    background-size: cover;
  }

  .carousel-3d-container {
    width: 900px;
    position: relative;
    margin-bottom: 20px;
  }

  .carousel-3d-slide {
    height: 550px !important;
    margin-top: 20px;
  }
  
  .crs-bx {
    padding-top: 20px;
    text-align: center;
    vertical-align: middle;
    border: solid 2px #000;
    background-color: white;
    height: 530px;
  }

  .grade-img {
    padding: 30px;
    border: solid 3px #E2E2E2;
    width: 250px;
    height: 250px;
  }

  .text-box {
    margin: 20px;
    height: 186px;
  } 

  .grade-guide {
    position: relative;
    bottom: 10px;
    padding: 0px;
  }

.square{
  border:0;
  width:80px;
  padding:0px;
  margin-top: 150px;
  margin-left: 360px;
  margin-left: -webkit-calc(50% - 40px);
  margin-left: -moz-calc(50% - 40px);
}

.spin {
  height: 130px;
  width: 130px;
  border-radius: 50%;
  border:dashed 5px white;
  -webkit-animation-name: spin;
  -webkit-animation-duration: 1.5s;
  -webkit-animation-iteration-count: infinite;
  -webkit-animation-timing-function: linear;
}

@-webkit-keyframes spin {
  from   {  -webkit-transform: rotate(0deg); }
  to   {  -webkit-transform: rotate(360deg); }
}

</style>