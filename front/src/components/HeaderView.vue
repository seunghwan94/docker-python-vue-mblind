<template>
  <nav class="navbar navbar-expand-lg" style="width: 100%;">
    <div class="container-fluid">
      <a class="navbar-brand" href="#" @click.prevent="navigateTo('home')"><h1 class="text-success" style="font-weight:bold;">m-lind</h1></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor04" aria-controls="navbarColor04" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarColor04">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: MainMenu === 'home' }" href="#" @click.prevent="navigateTo('home')">홈</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: MainMenu === 'board' }" href="#" @click.prevent="navigateTo('board')">게시판</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: MainMenu === 'photo' }" href="#" @click.prevent="navigateTo('photo')">사진첩</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: MainMenu === 'chatting' }" href="#" @click.prevent="navigateTo('chatting')">채팅</a>
          </li>
        </ul>
        <div class="d-flex" style="margin: 10px 0 ">
          <img v-if="user_img" :src="require(`../assets/img/${user_img}`)" style="width: 35px;height:35px; border-radius: 50%; cursor: pointer;">
          <p v-if="user_name" class="text-body p-2 m-0">{{ user_name }} 님 안녕하세요. </p>
        </div>
        <button v-if="!user_id" type="button" class="btn btn-outline-success my-2 my-sm-0" @click="$emit('openModal')">login</button>
        <button v-else type="button" class="btn btn-outline-success my-2 my-sm-0" @click="$emit('openModal')">profile</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      user_id: sessionStorage.getItem('user_id'),
      user_name: sessionStorage.getItem('user_name'),
      user_img: sessionStorage.getItem('user_img'),
    }
  },
  methods: {
    navigateTo(tab) {
      this.$router.push(`/${tab}`);
      this.$emit('updateMainMenu', tab);
    }
  },
  props: {
    MainMenu: String,
  }
}
</script>
