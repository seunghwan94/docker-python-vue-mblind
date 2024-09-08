<template>
    <div class="login-contain">
        <div class="login-logo">
            <img src="../assets/img/logo.png" style="width:40%;"> 
            <h2  v-if="is_set==1" style="padding-right: 20px;">챗봇 아이디/비밀번호 찾기</h2>
            <h2  v-else-if="is_set==2" style="padding-right: 20px;">챗봇 회원가입</h2>
            <h2  v-else style="padding-right: 20px;">챗봇 로그인</h2>
        </div>
        <div class="login-body">
            <div v-if="is_set==1">
                <LoginFindView @defaultView="defaultView"/>
            </div>
            <div v-else-if="is_set==2">
                <LoginSignView @defaultView="defaultView"/>
            </div>
            <div v-else>
                <div class="login-group">
                    <span>ID</span>
                    <input v-model="id" type="text" class="login-id" placeholder="UserID" aria-label="UserID">
                </div>
                <div class="login-group">
                    <span>PW</span>
                    <input v-model="pw" type="password" class="login-pw" placeholder="UserPW" aria-label="UserPW">
                </div>
                <div v-if="error" class="error-message" style="margin-top: 10px;">{{ error }}</div>
                <div class="login-group">
                    <button @click="loginck">로그인</button>
                </div>

                <div class="login-group" style="justify-content:space-between;font-size: 13px;">
                    <a href="#" @click="is_set=1" style="color:gray">아이디/비밀번호 찾기</a>
                    <a href="#" @click="is_set=2" style="color:gray">회원 가입</a>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import LoginSignView from './LoginSignView.vue'
import LoginFindView from './LoginFindView.vue'
import axios from 'axios';
import { BackURL } from '../main.js';

export default {
    name:'LoginView',
    data(){
        return {
            id:'',
            pw:'',
            is_set:0,
            error: '',
        }
    },
    methods:{
        loginck(){
            if (!this.id) {
                this.error = '아이디를 입력하세요.';
                return;
            }
            if (!this.pw) {
                this.error = '비밀번호를 입력하세요.';
                return;
            }
            const userData = {
                id: this.id,
                pw: this.pw,
            };

            axios.post(BackURL+'/login', userData)
            .then(response => {
                console.log(response.data[0].id)
                sessionStorage.setItem('id', response.data[0].id);
                sessionStorage.setItem('user_id',this.id);
                sessionStorage.setItem('user_pw',this.pw);
            
                this.$router.push('/chat/main');
            })
            .catch(error => {
                // 회원가입 실패 처리
                console.error('로그인 실패:', error);
                this.error = error.response.data
                return;
            });
        },
        defaultView(){
            this.is_set=0;
        }
    },
    components:{
        LoginSignView,
        LoginFindView,
    }
}
</script>

<style>
.login-contain {
    background: #FCF6F1;
    border-radius: 5px;
    width: 100%;
    height: 100%;
}
.login-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 15%;
}
.login-body {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    margin-top: 40%;
}
.login-group {
    display: flex;
    align-items: center;
    margin: 5px;
    width: 100%; /* 부모 요소의 너비에 맞게 조정 */
    max-width: 300px; /* 최대 너비 설정 */
    justify-content: flex-end;
        color: #fff;
}
.login-group span {
    background: #a7c4e0;
    padding: 5px;
    font-size: 17px;
    border-radius: 5px 0 0 5px;
    display: inline-block;
    width: 50px;
    text-align: center;
    font-weight: bold;
}
.login-group input {
    padding: 5px;
    font-size: 17px;
    border-radius: 0 5px 5px 0;
    border: 1px solid transparent;
    width: calc(100% - 50px - 2px); /* 부모 요소의 너비에서 span 너비와 여백을 뺀 값 */
    margin-left: -1px; /* 테두리가 겹치지 않도록 조정 */
}
.login-group button {
    width: 100%;
    font-size: 17px;
    padding: 5px 10px;
    border-radius: 5px;
    border: 1px solid transparent;
    cursor: pointer; /* 커서 변경 */
    background:  #a7c4e0;
    color: #fff;
    font-weight: bold;
    margin-top: 20px;
}

.retrun-view {
    cursor: pointer;
    font-size: 13px;
    color:gray;
}
/* 일반적인 모바일 장치 */
@media (min-width: 321px) and (max-width: 480px) {
  body {
    background-color: #ffccdd;
  }
  
  .container {
    padding: 15px;
    font-size: 16px;
  }
}


</style>