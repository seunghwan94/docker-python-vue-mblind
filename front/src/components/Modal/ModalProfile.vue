<template>
    <div class="modal-body">
      <!-- tab -->
      <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item" role="presentation">
          <a class="nav-link" :class="{ active: activeTab === 'profile' }" data-bs-toggle="tab" href="#profile" @click="activeTab = 'profile'" aria-selected="false" role="tab" tabindex="-1">Profile</a>
        </li>
        <li class="nav-item" role="presentation">
          <a class="nav-link" :class="{ active: activeTab === 'ChangePW' }" data-bs-toggle="tab" href="#ChangePW" @click="activeTab = 'ChangePW'" aria-selected="true" role="tab">ChangePW</a>
        </li>
        <li class="nav-item" role="presentation">
          <a class="nav-link" :class="{ active: activeTab === 'Setting' }" data-bs-toggle="tab" href="#Setting" @click="activeTab = 'Setting'" aria-selected="true" role="tab">Setting</a>
        </li>
      </ul>
      <div id="myTabContent" class="tab-content">
        <!-- Profile -->
        <div class="tab-pane fade" :class="{ active: activeTab === 'profile', show: activeTab === 'profile' }" id="profile" role="tabpanel">
          <div class="card border-success m-3">
            <div class="d-flex w-100" style="justify-content:center;">
              <div v-if="isLoading" class="spinner-border text-success" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <img v-else-if='temp_user_img' class="w-50 mt-4" :src="require(`../../assets/img/${temp_user_img}`)" style="border-radius: 50%; cursor: pointer;" @click="$refs.imgFlie.click()">
              <img v-else class="w-50 mt-4" :src="require(`../../assets/img/${user_img}`)" style="border-radius: 50%; cursor: pointer;" @click="$refs.imgFlie.click()">
              <input type="file" ref="imgFlie" @change="onFileUpload" style="display: none;" accept="image/*">
            </div>
            <div class="card-body">
              <label class="form-label">이름</label>
              <div class="form-floating mb-3">
                <input type="text" class="form-control" id="user_name" v-model="user_name" placeholder="user_name">
                <label for="user_name">이름</label>
              </div>

              <div class="d-flex">
                <div class="me-3" style="width: 60%;">
                  <label class="form-label">생년월일 (ex.1994-03-27) </label>
                  <div class="form-floating mb-3">
                    <input type="date" class="form-control" id="user_birth" v-model="user_birth" placeholder="user_birth">
                    <label for="user_birth">생년월일</label>
                  </div>
                </div>
                <div style="width: 35%;">
                  <label class="form-label"> 성별 </label>
                  <div class="form-floating mb-3">
                    <select class="form-control" id="user_gender" v-model="user_gender">
                      <option value="" disabled selected>성별 선택</option>
                      <option value="male">남성</option>
                      <option value="female">여성</option>
                      <option value="other">기타</option>
                    </select>
                    <label for="user_gender">성별</label>
                  </div>
                </div>
              </div>

              <div class="form-floating mb-3">
                <input type="text" class="form-control" id="user_addr" v-model="user_addr" placeholder="user_addr">
                <label for="user_addr">주소</label>
              </div>

              <div class="form-floating mb-3">
                <textarea class="form-control" id="user_intro" v-model="user_intro" placeholder="user_intro"></textarea>
                <label for="user_intro">자기소개</label>
              </div>

                <!-- 오류 메시지 -->
              <div v-if="errorMessage" class="alert alert-danger m-3">
                <strong>{{ errorMessage }}</strong>
              </div>
              <div class="d-flex m-3" style="justify-content: center;">
                <button type="button" class="btn btn-success" id="profileModify" @click="profileChange">변경하기</button>
              </div>
            </div>
          </div>
        </div>
        <!-- ChangePW -->
        <div class="tab-pane fade" :class="{ active: activeTab === 'ChangePW', show: activeTab === 'ChangePW' }" id="ChangePW" role="tabpanel">
          <div class="card border-success m-3" style="padding:16px">
            <label class="form-label mt-4">비밀번호 변경</label>
            <div class="form-floating">
              <input type="password" class="form-control" id="LoginPW" v-model="loginPW" placeholder="LoginPW" autocomplete="off">
              <label for="LoginPW">기존 비밀번호를 입력하세요.</label>
            </div>
            <div class="form-floating mt-4">
              <input type="password" class="form-control" id="newLoginPW" v-model="newLoginPW" placeholder="LoginPW" autocomplete="off">
              <label for="newLoginPW">새 비밀번호를 입력하세요.</label>
            </div>
            <div class="form-floating mt-4">
              <input type="password" class="form-control" id="newLoginPWChack" v-model="newLoginPWChack" placeholder="LoginPW" autocomplete="off">
              <label for="newLoginPWChack">새 비밀번호 확인</label>
            </div>
            <!-- 오류 메시지 -->
            <div v-if="errorMessage" class="alert alert-danger m-3">
              <strong>{{ errorMessage }}</strong>
            </div>
            <div class="d-flex m-3" style="justify-content: center;">
              <button type="button" class="btn btn-success" @click="pwChange">비밀번호 변경하기</button>
            </div>
          </div>
        </div>
        <!-- Setting -->
        <div class="tab-pane fade" :class="{ active: activeTab === 'Setting', show: activeTab === 'Setting' }" id="Setting" role="tabpanel">
          <div class="card border-success m-3" style="padding:16px">
            <legend class="mt-2">Theme 변경</legend>
            <!-- 테마 목록을 반복하여 라디오 버튼 생성 -->
            <div class="d-flex" style="flex-wrap: wrap;">
              <div v-for="(theme,index) in ThemeList_arr" :key="index" class="form-check m-1">
                <input
                  class="form-check-input"
                  type="radio"
                  :name="'themeOptions'"
                  :id="'optionsRadios' + index"
                  :value="index"
                  v-model="selectedTheme"
                >
                <label class="form-check-label" :for="'optionsRadios' + index">
                  {{ theme.theme }}
                </label>
              </div>
            </div>
            <div class="d-flex m-3" style="justify-content: center;">
                <button type="button" class="btn btn-success" @click="changeTheme">변경하기</button>
              </div>
            <div class="d-flex m-3" style="justify-content:center;">
              <button type="button" class="btn btn-success" @click="logout">logout</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import axios  from 'axios';

  export default {
    name: 'ModalProfile',
    data() {
      return{
        activeTab: 'profile',
        user_id: sessionStorage.getItem('user_id'),
        user_name: sessionStorage.getItem('user_name'),
        user_img: sessionStorage.getItem('user_img'),
        user_birth: '',
        user_gender: '',
        user_addr: '',
        user_intro: '',
        temp_user_img : '',
        isLoading: false,  // 로딩 상태 변수 추가
        ThemeList_arr: [],
        selectedTheme: null,
      }
    },
    mounted() {
      this.themeList();
      this.profileLoad();
    },
    methods: {
      themeList() {
        axios.post(`${this.$BackURL}/themeList`, {
          user_id: this.user_id
        }).then(response => {
          console.log(response.data);
          if (response.data.status == 'success') {
            this.ThemeList_arr = response.data.res;
          } else {
            console.log('오류발생 새로고침해주세요.');
          }
        }).catch(error => {
          alert('Theme오류 새로고침해주세요.');
          console.error('Error uploading file:', error);
        }).finally(() => {
          // this.isLoading = false;  // 로딩 종료
        });
      },
      changeTheme() {
        if (this.selectedTheme) {
          axios.post(`${this.$BackURL}/selectTheme`, {
            user_id: this.user_id,
            theme_id: this.selectedTheme
          }).then(response => {
            console.log(response.data);
            if (response.data.status == 'success') {
              alert(`테마가 수정되었습니다.새로고침해주세요.`);
            } else {
              console.log('오류발생 새로고침해주세요.');
            }
          }).catch(error => {
            alert('Theme오류 새로고침해주세요.');
            console.error('Error uploading file:', error);
          });
        } else {
          alert('테마를 선택해주세요.');
        }
      },
      profileLoad(){
        axios.post(`${this.$BackURL}/profileLoad`, {
          user_id: this.user_id
        }).then(response => {
          if (response.data.status == 'success') {
            this.user_birth = response.data.res[0].birth;
            this.user_gender = response.data.res[0].gender;
            this.user_addr = response.data.res[0].addr;
            this.user_intro = response.data.res[0].intro;
            this.selectedTheme = response.data.res[0].theme_id;
          } else {
            console.log('오류발생 새로고침해주세요.');
          }
        }).catch(error => {
          alert('Theme오류 새로고침해주세요.');
          console.error('Error uploading file:', error);
        })
      },
      logout() {
        if (confirm('logout을 진행하시겠습니까?')) {
          sessionStorage.removeItem('user_id');
          sessionStorage.removeItem('user_name');
          sessionStorage.removeItem('user_img');
          
          this.user_id = null;
          this.user_name = null;
          this.user_img = null;
          
          window.location.reload();
        }
      },
      onFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
          const formData = new FormData();
          formData.append('file', file);

          this.isLoading = true;  // 로딩 시작
          document.getElementById('profileModify').disabled = true;
          axios.post(`${this.$BackURL}/UploadFile`, formData)
            .then(response => {
              if (response.data.success) {
                this.temp_user_img = response.data.filename;
              } else {
                alert('파일 업로드 실패');
              }
            }).catch(error => {
              alert('파일 업로드 중 오류 발생');
              console.error('Error uploading file:', error);
            }).finally(() => {
              document.getElementById('profileModify').disabled = false;
              this.isLoading = false;  // 로딩 종료
          });
        }
      },
      profileChange() {
        if(confirm('수정하시겠습니까?')){
          let temp_img_name;

          if(this.temp_user_img==''){
            temp_img_name = this.user_img;
          }else{
            temp_img_name = this.temp_user_img;
          }
          axios.post(`${this.$BackURL}/profileChange`, {
            img_name: temp_img_name,
            user_id : this.user_id,
            user_name : this.user_name,
            user_birth: this.user_birth,
            user_gender: this.user_gender,
            user_addr: this.user_addr,
            user_intro: this.user_intro,
          }).then(response => {
            if (response.data.status == 'success') {
              sessionStorage.setItem('user_img',temp_img_name);
              sessionStorage.setItem('user_name',this.user_name);
              this.user_img = temp_img_name;
              this.temp_user_img = '';
              alert('변경 되었습니다.');
            } else {
              console.log(response.data,);
              alert('파일 업로드 실패');
            }
          }).catch(error => {
            console.error('Error uploading file:', error);
          });
        }
      },
      pwChange() {
        if(this.loginPW==undefined){
          alert('공백');
          return;
        }
        if(this.newLoginPW != this.newLoginPWChack) {
          alert('새 비밀번호 일치하지 안습니다.')  ;
          return;
        }

        if(confirm('수정하시겠습니까?')){
          axios.post(`${this.$BackURL}/pwChange`, {
            user_id : this.user_id,
            user_pw : this.newLoginPW
          }).then(response => {
            if (response.data.status == 'success') {
              alert('비밀번호가 변경 되었습니다.');
              this.activeTab='profile';
            } else {
              console.log(response.data,);
              alert('비밀번호 변경 실패');
            }
          }).catch(error => {
            console.error('Error uploading file:', error);
          });
        }
      }
    }
  };
  </script>
  
  <style>

  </style>