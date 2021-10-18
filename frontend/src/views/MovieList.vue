<template> 
    <div>
    <b-card-group deck v-for="Data in splitdata" :key="Data.id">
        <b-card v-for="item in Data" :key="item.id"
            tag="article"
            class="mb-2"
        >
            <span v-if="$route.params.part == 'title'">
                <b-card-title style="font-size: 1.2rem">
                {{maketitle(item.title)}}
                </b-card-title>
                <b-card-img :src="'http://image.tmdb.org/t/p/w200'+item.poster_path"
                style="width: 260px; height: 390px"></b-card-img>
                <b-card-text>
                {{item.overview.substring(0,35)+'...'}}
                </b-card-text>
            </span>
            <span v-else>
                <b-card-title style="font-size: 1.2rem">
                {{maketitle(item.ko_name)}}
                </b-card-title>
                <div style="margin-top:10px"></div>
                <b-card-img :src="'http://image.tmdb.org/t/p/w200'+item.profile_path"
                style="width: 260px; height: 390px"></b-card-img> 
                <div style="margin-top:10px"></div>
            </span>


            <b-button @click="godetail(item.id,$route.params.part)">Go Detail</b-button>
        </b-card>
    </b-card-group>
    </div>
</template>

<script>
import axios from 'axios'
const cors = require('cors');

// Vue.use(cors()); /* 1번*/
export default {
    data() {
        return {
            Data: [],
            splitdata: []
        }
    },
    methods: {
        GetData() {
            axios.get(this.$store.state.base_url+'/movie/search/'+this.$route.params.part+'/'+this.$route.params.keyword,{params:{}})
            .then((response) => {
                this.Data = response.data
                for (var i = 0; i < this.Data.length/4+1; i++){
                    this.splitdata.push(this.Data.slice(4*i,4*(i+1)))
                } 
            })
            .catch((error) => {
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
        }
    },
    created() {
        this.GetData();
    },   
}
</script>

<style scoped>

.h4{
    font-size: 1.3rem !important;
}

</style>

