<template>

    <span v-if="$route.params.part == 'title'">
      <div id="mainContainer">
      <img :src="this.moviedata.poster_path" id="poster">
      <div id="info">
        <h1>{{this.moviedata.title}}</h1>
        <h4>{{this.moviedata.release_date + '/' + this.moviedata.genre + '/' + this.moviedata.runtime+'분'}}</h4>
        <div style="margin-top: 10px; margin-left: 10px">
          <v-rating v-model="rating" size="30" style="display:inline-block"></v-rating>
          <v-btn rounded color="primary" style="margin-left:50px" @click="goadd(moviedata.id)">평가하기</v-btn>
        </div>

        <p>감독 : {{this.moviedata.director}}</p>
        <p>{{this.moviedata.overview}}</p>

        <div></div>
      </div>
      </div>
    </span>
    <span v-else-if="$route.params.part == 'actor'">
      <div id="actorContainer">
      <img :src="this.moviedata.profile_path" id="poster">
      <div id="info">
        <h1>{{this.moviedata.name}}</h1>
        <h4>{{this.moviedata.birthday + '/' + this.moviedata.gender}}</h4>
        <div style="margin-top: 10px; margin-left: 10px">
          <v-rating v-model="rating" size="30" style="display:inline-block"></v-rating>
          <v-btn rounded color="primary" style="margin-left:50px" @click="goadd(moviedata.id)">평가하기</v-btn>
        </div>

        <!-- <p>감독 : {{this.moviedata.director}}</p>
        <p>{{this.moviedata.overview}}</p> -->

        <div></div>
      </div>  
      </div>
          <b-card-group deck v-for="Data in splitdata" :key="Data.id">
        <b-card v-for="item in Data" :key="item.id"
            tag="article"
            class="mb-2"
        >
                <b-card-title style="font-size: 1.2rem">
                {{maketitle(item.title)}}
                </b-card-title>
                <b-card-img :src="'http://image.tmdb.org/t/p/w200'+item.poster_path"
                style="width: 260px; height: 390px"></b-card-img>
                <b-card-text>
                {{item.overview.substring(0,35)+'...'}}
                </b-card-text>

            <b-button @click="godetail(item.id,'title')">Go Detail</b-button>
        </b-card>
    </b-card-group>
    </span>
    <span v-else>
      <div id="actorContainer">
      <img :src="this.moviedata.profile_path" id="poster">
      <div id="info">
        <h1>{{this.moviedata.name}}</h1>
        <h4>{{this.moviedata.birthday + '/' + this.moviedata.gender}}</h4>
        <div style="margin-top: 10px; margin-left: 10px">
          <v-rating v-model="rating" size="30" style="display:inline-block"></v-rating>
          <v-btn rounded color="primary" style="margin-left:50px" @click="goadd(moviedata.id)">평가하기</v-btn>
        </div>

        <!-- <p>감독 : {{this.moviedata.director}}</p>
        <p>{{this.moviedata.overview}}</p> -->

        <div></div>
      </div>  
      </div>
          <b-card-group deck v-for="Data in splitdata" :key="Data.id">
        <b-card v-for="item in Data" :key="item.id"
            tag="article"
            class="mb-2"
        >
                <b-card-title style="font-size: 1.2rem">
                {{maketitle(item.title)}}
                </b-card-title>
                <b-card-img :src="'http://image.tmdb.org/t/p/w200'+item.poster_path"
                style="width: 260px; height: 390px"></b-card-img>
                <b-card-text>
                {{item.overview.substring(0,35)+'...'}}
                </b-card-text>

            <b-button @click="godetail(item.id,'title')">Go Detail</b-button>
        </b-card>
    </b-card-group>
    </span>

</template>

<script>
import axios from 'axios'

export default {
  data(){
    return {
      moviedata : {},
      rating : 5,
      splitdata: []
    }
  },
  created(){
    this.getdetail(this.$route.params.part,this.$route.params.movieid)
  },
  beforeRouteUpdate (to, from, next){
      this.getdetail(to.params.part,to.params.movieid);
      next();
  },
  methods: {
    getdetail(part,id){
      console.log(part,id)
      let uri = ''
      if (part == 'title'){
        uri = this.$store.state.base_url+'/movie/'+id
        axios.get(uri)
        .then((response) => {
          this.moviedata = {
            'title' : response.data.title,
            'overview' : response.data.overview,
            'keyword' : response.data.keyword,
            'runtime' : response.data.runtime,
            'poster_path' : 'http://image.tmdb.org/t/p/w400' + response.data.poster_path,
            'actor' : response.data.actor_string.split('|'),
            'director' : response.data.director_string,
            'release_date' : response.data.release_date,
            'tagline' : response.data.tagline,
            'keyword' : response.data.keyword.split('|'),
            'genre' : response.data.genre_string,
            'id': response.data.id
          }
          axios.post(this.$store.state.base_url+'/search/save/',{
            'id': this.moviedata.id,
            'keyword': 'movie',
            'word': this.moviedata.title,
            'user_id': this.$cookies.get('userid')})
          .then((response) => {
            console.log('movie save')
          })
        })
        .catch((error) =>{
          console.log(error)
        })
      }
      else if (part == 'actor') {
        uri = this.$store.state.base_url+'/movie/search/'+part+'/detail/'+id
        axios.get(uri)
        .then((response) => {
          let data = response.data[0]
          console.log(data)
          let gender = '남성'
          if (data.gender == 1){
            gender = '여성'
          }
          this.moviedata = {
            'name' : data.ko_name + ' ' + data.name,
            'birthday' : data.birthday,
            'profile_path' : 'http://image.tmdb.org/t/p/w400' + data.profile_path,
            'gender' : gender,
            'id': data.id,
            'movielist': data.actor_movies
          }
          for (var i = 0; i < data.actor_movies.length/4+1; i++){
              this.splitdata.push(data.actor_movies.slice(4*i,4*(i+1)))
          }
          axios.post(this.$store.state.base_url+'/search/save/',{
            'id': this.moviedata.id,
            'keyword': 'actor',
            'word': this.moviedata.name,
            'user_id': this.$cookies.get('userid')})
          .then((response) => {
            console.log('actor save')
          })
        })
        .catch((error) =>{
          console.log(error)
        })
      }
      else   {
        uri = this.$store.state.base_url+'/movie/search/'+part+'/detail/'+id
        axios.get(uri)
        .then((response) => {
          let data = response.data[0]
          console.log(data)
          let gender = '남성'
          if (data.gender == 1){
            gender = '여성'
          }
          this.moviedata = {
            'name' : data.ko_name + ' ' + data.name,
            'birthday' : data.birthday,
            'profile_path' : 'http://image.tmdb.org/t/p/w400' + data.profile_path,
            'gender' : gender,
            'id': data.id,
            'movielist': data.director_movies
          }
          for (var i = 0; i < data.director_movies.length/4-1; i++){
              this.splitdata.push(data.director_movies.slice(4*i,4*(i+1)))
          }
          axios.post(this.$store.state.base_url+'/search/save/',{
            'id': this.moviedata.id,
            'keyword': 'director',
            'word': this.moviedata.name,
            'user_id': this.$cookies.get('userid')})
          .then((response) => {
            console.log('director save')
          })
        })
        .catch((error) =>{
          console.log(error)
        })
      }
    },
    goadd(movieid) {
      axios.post(this.$store.state.base_url+'/movie/add/',{
        'user': this.$cookies.get('userid'),
        'movie': movieid,
        'rating': this.rating
      })
      .then((response) => {
        alert('평가에 반영되었습니다.')
      })
      .catch((error) =>{
        console.log(error)
      })
    },
    maketitle(title){
        let temp = ''
        if (title.length > 40){
            let temp = title.substring(0,30) +'...'
        }
        else {
            temp = title
            while (temp.length < 40){
                temp = temp + ' '
            }
        }
        return temp
    },
    godetail(id,part){
      this.$router.push('/detail/'+id+'/'+part)
    },
  }
}
</script>

<style scoped>
*{
  margin:0;
  padding:0;
  font-family: 'Dosis', sans-serif;
}
body{
  background:#232323;
}
#mainContainer{
  margin-top: 100px;
  width:900px;
  height:600px;
  margin:0 auto;
  display:flex;
  box-sizing:border-box;
/*   box-shadow:0 0 30px #fff; */
}
#actorContainer{
  margin-top: 100px;
  width:900px;
  height:600px;
  margin:0 auto;
  display:flex;
  box-sizing:border-box;
/*   box-shadow:0 0 30px #fff; */
}

#poster{
  width:400px;
  height:inherit;
  background-size:cover;
}
#info{
  width:500px;
  box-sizing:border-box;
  padding:30px;
  background-color:#fff;
}
#info > h1{
  font-size:40px;
  letter-spacing:2px;
  margin-bottom:12px;
}
#info > h4{
  letter-spacing:3px;
  padding-bottom:10px;
  border-bottom:2px solid #000;
  box-sizing:border-box;
  color:#2ecc71;
}
#info > p{
  line-height:1.6em;
  width:400px;
  margin:0 auto;
  margin-top:10px;
  letter-spacing:2px;
}
.bottom{
  height:75px;
  position:relative;
  top:150px;
  border-top:2px solid;
  box-sizing:border-box;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.bottom >div{
  height:60px;
  width:190px;
  display:flex;
  justify-content:space-around;
  align-items:center;
}
.bottom >div > div{
  display:flex;
  width:50px;
  justify-content:space-around;
  align-items:center;
  cursor:pointer;
}

/* star */
.ratized input[type="radio"]:checked+label:before {
    position: absolute;
    top: 0;
    right: 2px;
}

.ratized {
    position: relative;
}

.ratized input[type="radio"] {
  position: fixed;
  top: 0;
  right: 100%;
}


.ratized label {
  font-size: 1.8em;
  cursor: pointer;
}

.ratized input[type="radio"]:checked ~ input + label {
  background: none;
  color: #aaa;
}

.ratized input + label {
  color: orange;
}


/* ----- DEMO STUFF ----- */
body {
  background: #888;
  color: #fff;
  text-align:center;
}

</style>