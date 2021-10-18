<template>
    <div class="container">
       <h1 class="logo">🗣COMMUNITY</h1>


        <div class="que" v-for="item in list" :key="item.id"  >
        <div class="stats">
            <h6 style="text-size:small;">댓글수</h6>
            <div class="like">
            <strong>0</strong>
            <span>개</span>
            </div>
        </div>
        <div class="summary">
            <div class="title-detail" style="text-align:left"><a class="tt title-detail" @click="detail(item.queNo,item.lang)">{{item.title}}</a></div>
            <div class="text">
            {{item.body}}
            </div>
            <div class="others">
            <span class="writerlabel">작성자</span>
            <a @click="userdetail()" class="writer nickname-in-detail">{{item.user}}</a>
            <span class="date">{{item.createDate}}</span>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data(){
        return {
            Data: [
                {
                    'id': 1,
                    'rpCnt':3,
                    'title': '반갑습니다',
                    'contents': '안녕하세요',
                    'queNo': 1,
                    'lang': '한국어',
                    'userNo': 3,
                    'name': '도정우',
                    'createDate': '23'
                }
            ],
            list : []
        }
    },
    methods: {
      getlist() {
      axios.get(this.$store.state.base_url +'/review/')
      .then((response) => {
        this.list = response.data
      })
      .catch((error) => {
        console.log(error)
      })
      },
      userdetail(){

      }
    },
    created() {
      this.getlist()
    }
}
</script>

<style scoped>

            @font-face {
    font-family: 'CookieRun-Regular';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/CookieRun-Regular.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}

@font-face { font-family: 'TmoneyRoundWindExtraBold'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-07@1.0/TmoneyRoundWindExtraBold.woff') format('woff'); font-weight: normal; font-style: normal; }


  * {
 font-family: 'TmoneyRoundWindExtraBold';  }

  .container{
    padding-left: 130px;
    padding-right: 130px;
  }
  .que{
    display: flex;
    padding: 12px 8px;
    float: none;
    overflow: hidden;
    border-bottom: 1px solid black;
  }
  .stats{
    margin-right: 12px;
    width: 58px;
    float: none;
    text-align: center;
    width: 60px;
    overflow-x:auto;
    overflow-y:auto;
    /* margin-bottom: 8px; */
    line-height:3em;
  }
  .like{
    padding: 7px 0 5px;
    /* border-radius: 3px; */
    background-color:white;
    border-top: 9px dashed black;
    border-bottom: 9px dashed black;   
    border-left: 2px solid black;
    border-right: 2px solid black;

  }
  .summary{
    overflow-x:auto;
    overflow-y:auto;
    flex: 1 auto;
    width: 100px;
    float: none;
    margin: 0;
    margin-left: 3%;
    margin-right: 3%;
    overflow: hidden;
  }
  .tt{
    font-weight: 400;
    word-wrap: break-word;
    word-break: break-word;
    font-size: 25px;
    line-height: 1.4;
    margin-bottom: .5em;
  }
  .contents{
    word-wrap: break-word;
    word-break: break-word;
    padding-bottom: 5px;
    height: 50px;
    overflow: hidden;
  }

  .tags{
    line-height: 18px;
    float: left;
  }
  .post-tag{
    font-size: 15px;
    color: cadetblue;
    font-family: 'TmoneyRoundWindExtraBold';
    background-color: rgb(211, 247, 247);
    border-color: transparent;
    display: inline-block;
    padding: .4em .5em;
    margin: 4px 4px 4px 4px;
    line-height: 1;
    white-space: nowrap;
    text-decoration: none;
    text-align: center;
    border-width: 1px;
    border-style: solid;
    border-radius: 30%;
  }
  .others{
    float: right;
    margin-right: 5%;

  }
  .writer{
    font-size: 14px;
    color: rgb(0, 0, 128);
    cursor: pointer;
    margin-right: 10px;
    margin-left: 10px;
  }
  .date{
    font-size: 12px;
  }
  .h1{
    color: cadetblue;
    background-color: rgb(211, 247, 247);
    border-color: transparent;
    display: inline-block;
    line-height: 1;
    white-space: nowrap;
    text-decoration: none;
    text-align: center;
    border-width: 1px;
    border-style: solid;
    border-radius: 30%;
  }
  .mainlang{
    margin-left: 25%;
  }
  .page-btn{
    padding-left: 5px;
    padding-right: 5px;
    font-size: 1.3em;
    color: pink;
  }
  .text{
    text-align:left; 
    min-height:50px; 
    margin-top:5px; 
    margin-bottom:10px
  }
  /* .pagination {
    display: inline-block;
  }
  .pagination button {
    color: black;
    float: left;
    padding: 8px 16px;
    text-decoration: none;
} */

.outter{
    position: fixed;
    right:50px;
    bottom:0;
    width: 190px;
    top: 200px
    }

.writerlabel {
  font-size: 0.9rem;
}

    .nickname-in-detail {
         font-family: 'TmoneyRoundWindExtraBold';
        color: rgb(0, 0, 128);
        font-size: 1.1rem;
    }

    .nickname-in-detail:hover {
        color: rgb(0, 0, 128);
    }

  .title-detail {
     font-family: 'TmoneyRoundWindExtraBold';
    color: rgb(0, 0, 128);
    font-size: 25px;   
    margin: 0;
    padding: 0;
  }

  .title-detail:hover {
      color: rgb(0, 0, 128);
  }

  .question-btn {
    position: absolute;
    display: block;
    top: 31%;
    right: 14%;
    width: 25%;
    z-index: 100;
  }

  .askbtn {
    cursor: pointer;
  }

   @media screen and (min-width: 1903px){

  .outter{
    position: fixed;
    right:30px;
    bottom:0;
    width: 130px;
    height: 500px;
    top: 200px
           /* padding: 150px 50px 0 0 */
    }
    .bannerimg{
      width: 130px;
      height: 500px;
    }
 }

  @media screen and (max-width: 1400px){
    .outter{
    position: fixed;
    right:50px;
    bottom:0;
    width: 150px;
    height: 500px;
    top: 200px
    }
    .bannerimg{
      width: 150px;
      height: 500px;
    }
  }

  @media screen and (max-width: 1000px){
    .outter{
    position: fixed;
    right:50px;
    bottom:0;
    width: 100px;
    height: 500px;
    top: 200px
    }
      .bannerimg{
      width: 100px;
      height: 500px;
    }
  }

  @media screen and (max-width: 770px){
    .outter{
      display: none;
    }
  }

  .logo {
    padding-top: 20px;
    font-size: 3rem;
}


</style>