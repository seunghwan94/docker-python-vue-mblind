<template>
    <div class="modal-body">
        <!-- tab -->
        <ul class="nav nav-tabs" role="tablist">
          <li class="nav-item" role="presentation">
              <a class="nav-link active" data-bs-toggle="tab" href="#login" aria-selected="false" role="tab" tabindex="-1">Login</a>
          </li>
          <li class="nav-item" role="presentation">
              <a class="nav-link" data-bs-toggle="tab" href="#signUp" aria-selected="true" role="tab">Sign Up</a>
          </li>
        </ul>
        <div id="myTabContent" class="tab-content">
          <!-- 로그인 -->
          <div class="tab-pane fade active show" id="login" role="tabpanel">
              <div class="card border-success m-3">
              <h1 class="text-success text-center m-5" style="font-weight:bold;">m-lind</h1>
              <div class="card-body">
                  <div class="form-floating mb-3">
                  <input type="email" class="form-control" id="LoginID" v-model="loginID" placeholder="LoginID">
                  <label for="LoginID">아이디를 입력하세요.</label>
                  </div>
                  <div class="form-floating">
                  <input type="password" class="form-control" id="LoginPW" v-model="loginPW" placeholder="LoginPW" autocomplete="off">
                  <label for="LoginPW">비밀번호를 입력하세요.</label>
                  </div>
                  <!-- 오류 메시지 -->
                  <div v-if="errorMessage" class="alert alert-danger m-3">
                  <strong>{{ errorMessage }}</strong>
                  </div>
                  <div class="d-flex m-3" style="justify-content: center;">
                  <button type="button" class="btn btn-success" @click="Login">Login</button>
                  </div>

              </div>
              </div>
          </div>
          <!-- 회원가입 -->
          <div class="tab-pane fade" id="signUp" role="tabpanel">
              <div class="card border-success m-3">
              <h1 class="text-success text-center m-5" style="font-weight:bold;">Sign Up</h1>
              <div class="card-body">
                  <!-- 이름 -->
                  <label class="form-label">
                  <p class="text-success m-0">회원님의 이름을 작성해주세요.</p>
                  </label>
                  <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="signUpName" v-model="signUpName" placeholder="signUpName">
                  <label for="signUpName">이름 입력</label>
                  </div>
                  <!-- 아이디 -->
                  <label class="form-label">
                  <p class="text-success m-0">회원 가입할 아이디를 입력하세요.</p>
                  </label>
                  <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="signUpID" v-model="signUpID" placeholder="signUpID">
                  <label for="signUpID">아이디 입력</label>
                  </div>
                  <!-- 비밀번호 -->
                  <label class="form-label">
                  <p class="text-success m-0">비밀번호를 입력하세요.</p>
                  </label>
                  <div class="form-floating mb-3">
                  <input type="password" class="form-control" id="signUpPW" v-model="signUpPW" placeholder="Password" autocomplete="off">
                  <label for="signUpPW">비밀번호 입력</label>
                  </div>
                  <!-- 비밀번호 확인 -->
                  <label class="form-label">
                  <p class="text-success m-0">비밀번호 확인</p>
                  </label>
                  <div class="form-floating">
                  <input type="password" class="form-control" id="confirmPW" v-model="confirmPW" placeholder="Password" autocomplete="off">
                  <label for="confirmPW">비밀번호 확인</label>
                  </div>
                  <div class="d-flex m-3" style="justify-content: center;">
                  <button type="button" class="btn btn-success" @click="SignUp">Sign Up</button>
                  </div>

              </div>
              </div>
          </div>
        </div>
    </div>
  </template>
  <script>
  import axios  from 'axios';

  export default {
    name: 'ModalLogin',
    data() {
      return {
        loginID: '',
        loginPW: '',
        errorMessage: ''
      };
    },
    methods: {
      Login() {
        if (this.loginID && this.loginPW) {
            axios.post(`${this.$BackURL}/login`, {
                loginID: this.loginID,
                loginPW: this.loginPW
            }).then(res => {
                console.log(res.data);
                if (res.data.status === 'success') {
                  sessionStorage.setItem('user_id', res.data.user_id);
                  sessionStorage.setItem('user_name', res.data.user_name);
                  sessionStorage.setItem('user_img', res.data.user_img);
                  this.errorMessage = '';
                  window.location.reload();
                }else{
                  this.errorMessage = '아이디 또는 비밀번호가 다릅니다.';
                }
            }).catch(e => {
                console.error('에러', e); 
                this.errorMessage = '서버에 연결할 수 없습니다.';
            });
        } else {
          this.errorMessage = '공백이 있습니다.';
        }
      },
      SignUp() {
        if (this.signUpName && this.signUpID && this.signUpPW && this.confirmPW) {
          if (this.signUpPW === this.confirmPW) {
            axios.post(`${this.$BackURL}/signUp`, {
              signUpID: this.signUpID,
              signUpPW: this.signUpPW,
              signUpName: this.signUpName
            }).then(res => {
              console.log(res.data);
              if (res.data.status === 'success') {
                this.signUpName = '';
                this.signUpID = '';
                this.signUpPW = '';
                this.confirmPW = '';
                this.errorMessage = '';

                alert('회원가입이 성공적으로 완료되었습니다.');

                // 로그인 탭으로 전환
                this.$nextTick(() => {
                  document.querySelector('a[href="#login"]').click();
                });
              } else {
                this.errorMessage = '존재하는 아이디입니다.';
              }
            }).catch(e => {
              console.error('에러', e); 
              this.errorMessage = '서버에 연결할 수 없습니다.';
            });
          } else {
            alert('비밀번호가 일치하지 않습니다.');
          }
        } else {
          alert('모든 필드를 채워주세요.');
        }
      }
    }
  };
  </script>
  
  <style>

  </style>