<template>
    <div class="main-profile-contain">
        <img :src="require(`../assets/img/${user.img}`)" @click="showModal = true" style="width:40%; border-radius: 50%; cursor: pointer;">
        <!-- <h2 style="margin:0px">{{ user.name }}</h2> -->
        <div style="display: flex; flex-direction: column; align-items: center;">
            <div class="login-group">
                <span>ID</span>
                <input v-model="user.user_id" type="text" class="login-id" placeholder="UserID" aria-label="UserID" readonly>
            </div>
            <div class="login-group">
                <span>PW</span>
                <input v-model="user.user_pw" type="text" class="login-pw" placeholder="UserPW" aria-label="UserPW">
            </div>
            <div class="login-group">
                <span style="width: 70px;">Name</span>
                <input v-model="user.name" type="text" class="login-name" placeholder="name" aria-label="name">
            </div>
            <div class="login-group">
                <span>Birth</span>
                <input v-model="user.birth" type="text" class="login-birth" placeholder="birth" aria-label="birth">
            </div>
            <div class="login-group">
                <span style="width: 90px;">Comments</span>
                <input v-model="user.comments" type="textarea" class="login-comments" placeholder="comments" aria-label="comments">
            </div>

            <div class="login-group">
                <button @click="$emit('profileEdit', user)">회원 정보 수정</button>
            </div>
        </div>
        <MainProfileImgView :images="imageList" :visible="showModal" @updateImage="updateImage" @close="showModal = false"/>
    </div>
</template>

<script>
import MainProfileImgView from './MainProfileImgView.vue';

export default {
    props: {
        list: Object
    },
    data() {
        return {
            user: { ...this.list },
            showModal: false,
            imageList: this.getImages()
        };
    },
    methods: {
        getImages() {
            const context = require.context('../assets/img', false, /\.png$/);
            return context.keys().map(key => {
                return {
                    src: context(key),
                    name: key.replace('./', '')
                };
            });
        },
        updateImage(selectedImage) {
            this.user.img = selectedImage.name;
            this.showModal = false;
        }
    },
    components: {
        MainProfileImgView,
    }
}
</script>

<style>
.main-profile-contain {
    background: #cbdced;
    padding: 15px;
    align-items: center;
    height: 95%;
}
</style>
