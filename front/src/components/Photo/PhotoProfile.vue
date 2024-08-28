<template>
    <div class="containercard card border-primary m-3" @mousemove="handleMouseMove" @mouseout="handleMouseOut" ref="container" @click="openModal">
      <div class="card-header">{{ userprofile.name }}</div>
      <div class="overlay" ref="overlay"></div>
      <!-- <div class="cardtest"></div> -->
      <img class="cardimg" :src="require(`../../assets/img/${userprofile.img}`)">
      <div class="card-body pt-2">
        <p class="card-text pt-1 m-0">생일 : {{ userprofile.birth }}</p>
        <p class="card-text pt-1 m-0">성별 : {{ userprofile.gender }}</p>
        <p class="card-text pt-1 m-0">주소 : {{ shortViewData(userprofile.addr) }}</p>
        <p class="card-text pt-1 m-0">자기소개 : {{ shortViewData(userprofile.intro) }}</p>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modalPhoto" class="modal" style="display: block;" tabindex="-1" role="dialog">
      <div class="modalcontainercard">
          <div class="containercard card border-primary m-3" style="width: 360px;" @mousemove="handleMouseMove" @mouseout="handleMouseOut" ref="container" @click="closeModal">
            <div class="card-header">{{ userprofile.name }}</div>
            <div class="overlay" ref="overlay"></div>
            <img class="cardimg" :src="require(`../../assets/img/${userprofile.img}`)" style="height: auto;">
            <div class="card-body pt-2">
              <p class="card-text pt-1 m-0">생일 : {{ userprofile.birth }}</p>
              <p class="card-text pt-1 m-0">성별 : {{ userprofile.gender }}</p>
              <p class="card-text pt-1 m-0">주소 : {{ userprofile.addr }}</p>
              <br/>
              <p class="card-text pt-2 pb-2 m-0">자기소개 <br/><br/> {{ userprofile.intro }}</p>    
            </div>
          </div>
      </div>
    </div>

  </template>
  
  <script>
  export default {
    data() {
      return{
        modalPhoto: false,
      }
    },
    props:{
      userprofile:Object,
    },
    methods: {
      openModal(){
        this.modalPhoto = true;
      },
      closeModal(){
        this.modalPhoto = false;
      },
      handleMouseMove(e) {
        const container = this.$refs.container;
        const overlay = this.$refs.overlay;
        
        // 컨테이너의 크기를 동적으로 가져오기
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
  
        // 컨테이너의 너비와 높이를 기반으로 회전 각도 계산
        const rotateY = ((x / rect.width) - 0.5) * 30; // -15도 ~ 15도 범위로 회전
        const rotateX = ((y / rect.height) - 0.5) * -30; // -15도 ~ 15도 범위로 회전

        container.style.transform = `perspective(350px) rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
        // 오버레이 배경 위치 및 효과 동적 적용
        overlay.style.backgroundPosition = `${(x / rect.width) * 100}% ${(y / rect.height) * 100}%`;
        overlay.style.opacity = (x / rect.width) * 0.5 + 0.1; // 투명도 조정
        overlay.style.filter = `brightness(${1 + (x / rect.width) * 0.5})`; // 밝기 조정
      },
      handleMouseOut() {
        const container = this.$refs.container;
        const overlay = this.$refs.overlay;
  
        overlay.style.opacity = '0';
        container.style.transform = 'perspective(350px) rotateY(0deg) rotateX(0deg)';
      },
      shortViewData(text){
        if (text.length > 10) {
          text = text.substring(0, 10) + "...";
        }
        return text;
      }
    }
  }
  </script>
  
  <style scoped>
  .containercard {
    width: 220px;
    transition: all 0.1s;
    position: relative;
    transform-style: preserve-3d;
  }
  .cardimg {
    width: 100%;
    height: 200px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(105deg,
        transparent 35%,
        rgba(255, 219, 112, 0.1) 40%,
        rgba(255, 219, 112, 0.5) 45%,
        rgba(132, 50, 255, 0.5) 50%,
        rgba(132, 50, 255, 0.1) 55%,
        transparent 60%
    );
    mix-blend-mode: color-dodge;
    background-size: 200% 200%;
    background-position: 100%;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    pointer-events: none;
    opacity: 0;
    filter: blur(0.5px);
    transition: opacity 0.3s;
  }
  .modalcontainercard {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1050; /* 모달이 다른 요소 위에 표시되도록 z-index를 설정 */
      width: auto;
  }
  </style>