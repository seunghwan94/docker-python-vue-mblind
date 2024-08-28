<template>
  <div id="app">
    <!-- header -->
    <div class="header">
      <HeaderView @updateMainMenu="updateMainMenu" @openModal="openModal" :MainMenu="MainMenu"/>
    </div>
    <div class="body">
      <router-view></router-view>
    </div>
    <!-- footer -->
    <div class="footer">
      <FooterView/>
    </div>


    <!-- Modal -->
    <div v-if="modalStatus" class="modal" style="display: block;" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div style="display: flex;justify-content: flex-end;">
          <button type="button" class="btn-close" @click="this.modalStatus = false" aria-label="Close"></button>
        </div>
        <ModalLogin v-if="!user_id"/>
        <ModalProfile v-else/>
        </div>
      </div>
    </div>
    <!-- loading -->
    <div id="loading"><h1 class="text-success" style="font-weight:bold;">Loading...</h1></div>
  </div>
</template>

<script>
import axios  from 'axios';
import HeaderView from './components/HeaderView.vue';
import FooterView from './components/FooterView.vue';
import ModalLogin from './components/Modal/ModalLogin.vue';
import ModalProfile from './components/Modal/ModalProfile.vue';

export default {
  name: "App",
  data() {
    return{
      MainMenu: 'home',
      modalStatus: false,
      user_id: sessionStorage.getItem('user_id'),
    }
  },
  mounted() {
    this.loadTheme();
  },
  methods: {
    openModal() {
      this.modalStatus = true;
    },
    async loadTheme() {
      try {
        const response = await axios.post(`${this.$BackURL}/Theme`,{
          user_id : this.user_id,
        });
        const data = response.data;
        if (data.status === 'success') {
          this.updateTheme(data.res[0].url);
        } else {
          console.error('Failed to load theme:', data.message);
        }
      } catch (error) {
        console.error('Error fetching theme:', error);
      }
    },
    updateTheme(url) {
      const linkTag = document.querySelector("link[rel=stylesheet]");
      if (linkTag) {
        linkTag.href = url;
      } else {
        const newLinkTag = document.createElement("link");
        newLinkTag.rel = "stylesheet";
        newLinkTag.href = url;
        document.head.appendChild(newLinkTag);
      }
      setTimeout(() => {
        document.getElementById('loading').style.display = 'none';  
      }, 300);
      
    },
    updateMainMenu(newMainMenu) {
      this.MainMenu = newMainMenu;
    },
  },
  components: {
    HeaderView,
    ModalLogin,
    FooterView,
    ModalProfile,
  }
};
</script>

<style>
/* 데스크탑 스타일 */
@media (min-width: 1024px) {
  .header, .body, .footer {
    padding: 0 200px;
  }
}

/* 태블릿 스타일 */
@media (min-width: 768px) and (max-width: 1023px) {
  .header, .body, .footer {
    padding: 0 50px;
  }
}

/* 모바일 스타일 */
@media (max-width: 767px) {
  .header, .body, .footer {
    padding: 0 20px;
  }

  .modal-dialog {
    max-width: 90%;
  }

}

#loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: white;
  color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.header{
  border-bottom: 1px solid lightgray;
}
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
}

.modal-dialog {
  max-width: 500px;
}

.modal-content {
  padding: 20px;
}
</style>
