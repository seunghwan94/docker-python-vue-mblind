<template>
    <div class="login-group">
        <span>ID</span>
        <input type="text" v-model="id" class="login-id" placeholder="아이디" aria-label="UserID">
    </div>
    <div class="login-group">
        <span>PW</span>
        <input type="password" v-model="pw" class="login-pw" placeholder="비밀번호" aria-label="UserPW">
    </div>
    <div class="login-group">
        <span style="width: 60px;">Name</span>
        <input type="text" v-model="name" class="login-name" placeholder="이름">
    </div>
    <div class="login-group">
        <span style="width: 90px;">BirthDay</span>
        <input type="text" v-model="birth" class="login-birth" placeholder="생년월일 (ex. 940327)">
    </div>
    <div class="login-group">
        <button @click="signup">회원가입</button>
    </div>
    <a class="retrun-view" @click="$emit('defaultView')">돌아가기</a>
    <div v-if="error" class="error-message">{{ error }}</div>
</template>

<script>
import axios from 'axios';
import { BackURL } from '../main.js';

export default {
    name:'LoginSignView',
    data(){
        return {
            id:'',
            pw:'',
            name: '',
            birth:'',
            error: ''
        }
    },
    methods:{
        signup(){

            // 유효성 검사
            if (!this.id) {
                this.error = '아이디를 입력하세요.';
                return;
            }
            if (!this.pw) {
                this.error = '비밀번호를 입력하세요.';
                return;
            }
            if (!this.name) {
                this.error = '이름을 입력하세요.';
                return;
            }
            const birthPattern = /^\d{6}$/;
            if (!birthPattern.test(this.birth)) {
                this.error = '생년월일은 6자리 숫자여야 합니다 (예: 940327).';
                return;
            }

            const userData = {
                id: this.id,
                pw: this.pw,
                name: this.name,
                birth: this.birth,
            };
            console.log(userData);

            axios.post(BackURL+'/signup', userData)
            .then(response => {
                console.log('회원가입 성공:', response.data);
                sessionStorage.setItem('id',this.id);
                this.$emit('defaultView');
            })
            .catch(error => {
                // 회원가입 실패 처리
                console.error('회원가입 실패:', error);
                this.error = error.response.data
                return;
            });
        }
    }
}
</script>

<style>

.error-message {
    color: red;
    margin-top: 10px;
}

</style>