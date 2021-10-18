<template>

<!-- <h1><img src="../assets/img/logo.PNG" alt=""></h1> -->
<div class="user" id="join"> 
    <div class="wrapC table">
        <div class="middle">
            <h1 class="logo">👪회원가입</h1>
            <div class="form-wrap">
                <div class="input-wrap">
                    <input v-model="nickName"
                        id="nickname"
                        placeholder="닉네임을 입력해주세요" type="text"/>
                </div>

                <div class="input-wrap">
                    <input v-model="email" 
                        id="email"
                        placeholder="이메일을 입력해주세요"
                        type="text"/>
                </div>

                <div class="input-wrap password-wrap">
                    <input v-model="password"
                        id="password" 
                        :type="passwordType"
                        placeholder="비밀번호를 입력해주세요"/>
                    <span :class="{active : passwordType==='text'}">
                            <i class="fas fa-eye"></i>
                        </span>
                </div>

                <div class="input-wrap password-wrap">
                    <input v-model="passwordConfirm" 
                        id="password-confirm"
                        :type="passwordConfirmType"
                        placeholder="비밀번호를 한번 더 입력해주세요"/>
                    <span :class="{active : passwordConfirmType==='text'}">
                            <i class="fas fa-eye"></i> 
                        </span>
                </div>
            </div>

            <label>
                <input v-model="isTerm" type="checkbox" id="term"/>
                <span>약관에 동의합니다</span>
            </label>

            <span class="go-term">약관 보기</span>

            <button class="btn btn-option" @click="signup">
                <span>
                    작성완료
                </span>
            </button>
        </div>


    </div> 
    

</div>
    

</template>

<script>
import '../assets/css/user.scss'
import axios from 'axios'
    export default {
        components: {
        },
        data: () => {
            return {
                email: '',
                nickName: '',
                password: '',
                passwordConfirm: '',
                isTerm: false,
                passwordType:"password",
                passwordConfirmType:"password",
            }
        },
        created(){
        },
        methods: {
            signup() {
                axios.post(this.$store.state.base_url+'/user/create/',
                {
                    email: this.email,
                    password: this.password,
                    nickname: this.nickName
                })
                .then((response) => {
                    alert('회원가입 되었습니다.')
                    axios.post(this.$store.state.base_url+'/user/login/',{
                        email:this.email,
                        password:this.password
                    })
                    .then((respose) => {
                        if (respose.data.success) {
                            this.$cookies.set('auth-token',respose.data.token)
                            this.$cookies.set('userid',respose.data.user_id)
                            this.$store.commit('checkToken',this.$cookies.get('auth-token'))
                            this.$store.commit('checklogin',this.$cookies.isKey('auth-token'))
                            this.$router.push('/start')
                        }
                        else {
                            alert('아이디 혹은 비밀번호를 확인하세요.')
                        }
                    })
                    .catch((error) => {
                        console.log(error)
                    })
                })
                .catch((error) => {
                    alert('이미 존재하는 이메일 입니다.')
                })
            }
        },
        watch: {
        },
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
