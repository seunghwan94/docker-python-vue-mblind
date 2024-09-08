<template>
    <div v-if="pw">
        <div class="error-message">ID : {{ id }}</div>
        <div class="error-message">PW : {{ pw }}</div>
        <div class="login-group">
            <button @click="$emit('defaultView')">돌아가기 </button>
        </div>
    </div>
    <div v-else>
        <div class="login-group">
            <span style="width: 60px;">Name</span>
            <input type="text" v-model="name" class="login-name" placeholder="이름">
        </div>
        <div class="login-group">
            <span style="width: 90px;">BirthDay</span>
            <input type="text" v-model="birth" class="login-birth" placeholder="생년월일 (ex. 940327)">
        </div>
        <div class="login-group">
            <button @click="findIdPw">아이디/비밀번호 찾기</button>
        </div>
        <a class="retrun-view" @click="$emit('defaultView')">돌아가기</a>
        <div v-if="error" class="error-message">{{ error }}</div>
    </div>
</template>

<script>
import axios from 'axios';
import { BackURL } from '../main.js';

export default {
    name:'LoginSignView',
    data(){
        return {
            name: '',
            birth:'',
            error: '',
            id: '',
            pw: ''
        }
    },
    props:{
        is_set:String,
    },
    methods:{
        findIdPw(){
            // 유효성 검사
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
                name: this.name,
                birth: this.birth,
            };

            axios.post(BackURL+'/findIdPw', userData)
            .then(response => {
                console.log('아이디:', response.data[0]);
                this.id = response.data[0]['user_id'];
                this.pw = response.data[0]['user_pw'];
            })
            .catch(error => {
                // 회원가입 실패 처리
                console.error('가입 내역 없음:', error);
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