<template>
<div class="container">

<h1 class="logo">✒ WRITING</h1>


  <link href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
<div class="container">

    <div class="wrapper">

        <div class="ccfield-prepend">
            <span class="ccform-addon"><i class="fa fa-info fa-2x"></i></span>
            <input class="ccformfield" v-model="title" type="text" placeholder="제목을 입력해주세요" required>
        </div>
        <div class="ccfield-prepend">
            <span class="ccform-addon"><i class="fa fa-comment fa-2x"></i></span>
            <textarea class="ccformfield" v-model="content" name="comments" rows="8" placeholder="내용을 입력해주세요" required></textarea>
        </div>
        <div class="ccfield-prepend-btn">
            <input class="ccbtn" type="submit" value="Submit" @click="submit">
        </div>
    </div>

    </div>
</div>



</template>

<script>
import axios from 'axios'
export default {
    data: () => {
        return {
            title: null,
            content: null
        }
    },
    methods: {
        submit() {
            let config = {
                headers: {
                    'Authorization' : 'jwt '+this.$cookies.get('auth-token')
                }
            }
            let body = {
                'title': this.title,
                'body': this.content,
                'user': this.$cookies.get('userid'),
                'movie': 155 
            }

            axios.post(this.$store.state.base_url+'/review/',body,config)
            .then((response) => {
                alert('성공적으로 작성 되었습니다.')
                this.$router.push('/list')
            })
            .catch((error) => {
                console.log(error)
            })
        }
    } 

}
</script>

<style scoped>
@font-face { font-family: 'TmoneyRoundWindExtraBold'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-07@1.0/TmoneyRoundWindExtraBold.woff') format('woff'); font-weight: normal; font-style: normal; }

@import url(https://fonts.googleapis.com/css?family=Lato:300,400,700);
body {
    background: #000000;
    color: #fff;
    font-weight: 400;
    font-size: 1em;
    font-family: 'Lato', Arial, sans-serif;
    margin:0;
    padding:0;
    padding-bottom:60px;
}

  .logo {
    padding-top: 20px;
    font-size: 3rem;
    font-family: 'TmoneyRoundWindExtraBold';
}
.ccheader {
    margin: 0 auto;
    padding: 2em;
    text-align: center;
}

.ccheader h1 {
    margin: 0;
    font-weight: 300;
    font-size: 2.5em;
    line-height: 1.3;
}
.ccheader {
    margin: 0 auto;
    padding: 2em;
    text-align: center;
}

.ccheader h1 {
    margin: 0;
    font-weight: 300;
    font-size: 2.5em;
    line-height: 1.3;
}

/* Form CSS*/
.ccform {
   margin: 0 auto;
    width: 800px;
}
.ccfield-prepend{
    margin-bottom:10px;
    width:100%;
}
.ccfield-prepend-btn{
    margin-bottom:10px;
    width:10%;
}

.ccform-addon{
    color:#000000; 
    float:left;
    padding:8px;
    width:5%;
    background:#FFFFFF;
    text-align:center;  
}

.ccformfield {
    color:#000000; 
    background:#FFFFFF;
    border:none;
    padding:15.5px;
    width:91.9%;
    display:block;
    font-family: 'Lato',Arial,sans-serif;
    font-size:14px;
}

.ccformfield {
    font-family: 'Lato',Arial,sans-serif;
}
.ccbtn{
    display:inline;
    margin-left: 970px;
    border:none;
    background:#000000;
    color:#FFFFFF;
    padding:12px 25px;
    cursor:pointer;
    text-decoration:none;
    font-weight:bold;
}
.ccbtn:hover{
    background:#000000;

}
.credit {
  color:#fff;
  width: 800px;
  clear:both;
margin:0 auto;
  line-height:25px;
 padding: 25px 50px; 
}
.credit em{
margin-right:5px;
}
.credit a {
color: #0d2ed5;
font-weight: bold;
text-decoration: none;
}


</style>