<template>

    <div class="user" id="login">
        <div class="wrapC table">
            <div class="middle">
                <h1 class="logo">🔑LOGIN</h1>
                <div class="input-wrap">
                    <input v-model="email"
                        id="email" 
                        placeholder="이메일을 입력해주세요"
                        type="text"/>
                </div>
                <div class="input-wrap">
                    <input v-model="password" type="password"
                        id="password"
                        placeholder="영문, 숫자 혼용 8자 이상"/>
                </div>
                <button class="btn btn--back btn--login btn-option" @click="login">
                    로그인 하기
                </button>
                <div class="add-option">
                    <div class="wrap">
                        <p>아직 회원이 아니신가요?</p>
                    </div>

                </div>
            </div>
            
        </div>
    </div>

</template>

<script>
    import '../assets/css/user.scss'
    import axios from 'axios'
    // import constants from '../lib/constants'
    
    export default {
        components: {
        },
        created(){
        },
        watch: {
        },
        methods: {
            login() {
                axios.post(this.$store.state.base_url+'/user/login/',{
                    email:this.email,
                    password:this.password
                })
                .then((respose) => {
                    console.log(respose)
                    if (respose.data.success) {
                        this.$cookies.set('auth-token',respose.data.token)
                        this.$cookies.set('userid',respose.data.user_id)
                        alert('로그인 되었습니다.')
                        this.$store.commit('checkToken',this.$cookies.get('auth-token'))
                        this.$store.commit('checklogin',this.$cookies.isKey('auth-token'))
                        this.$router.push('/')
                    }
                    else {
                        alert('아이디 혹은 비밀번호를 확인하세요.')
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
            }
        },
        data: () => {
            return {
                constants,
                email: '',
                password: '',

            }
        }

    }

</script>

<style scoped>
.logo {
    padding-top: 100px;
    font-size: 3rem;
}

.btn-option {
    height: 40px;
}

</style>