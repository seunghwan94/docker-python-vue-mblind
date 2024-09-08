<template>
    <div class="main-contain">

        <div v-if="is_set==0" class="main-header">
            <!-- <img :src="profileList.length > 0 ? require(`../assets/img/${profileList[0].img}`) : ''" style="width:20%;border-radius: 50%;"> -->
            <h2 style="padding-right: 20px;">대화방 들어가기</h2>
        </div>
        <div v-else-if="is_set!=1" class="main-header">
            <img :src="profileList.length > 0 ? require(`../assets/img/${profileList[0].img}`) : ''" style="width:20%;border-radius: 50%;">
            <h2 style="padding-right: 20px;">{{ profileList.length > 0 ? profileList[0].name : '' }}</h2>
        </div>


        <div v-if="is_set==0" class="main-body">
            <MainRoomListView v-for="(a, i) in chatList" :key="i" :list="a" @join_room="join_room"/>
        </div>
        <div v-if="is_set==1" class="main-body">
            <MainRoomView :RoomNumber="RoomNumber" :profileList="profileList" :otherUser="otherUser"/>
        </div>

        <div v-if="is_set==2" class="main-body">
            <MainUserView v-for="(a, i) in userList" :key="i" :list="a" @join_room_ck="join_room_ck"/>
        </div>
        <div v-else-if="is_set==3" class="main-body">
            <MainProfileView v-for="(a, i) in profileList" :key="i" :list="a" @profileEdit="profileEdit"/>
        </div>


        <div class="main-footer">
            <font-awesome-icon class="icon" :icon="['fas', 'bars']" size="2xl" @click="is_set=0"/>
            <font-awesome-icon class="icon" :icon="['fas', 'comment']" flip="horizontal" size="2xl" @click="is_set=1"/>
            <font-awesome-icon class="icon" :icon="['fas', 'magnifying-glass']" size="2xl" @click="is_set=2"/>
            <font-awesome-icon class="icon" :icon="['fas', 'user']" size="2xl" @click="is_set=3"/>
        </div>


    </div>
</template>

<script>
import axios from 'axios';
import MainProfileView from './MainProfileView.vue';
import MainUserView from './MainUserView.vue';
import MainRoomView from './MainRoomView.vue';
import MainRoomListView from './MainRoomListView.vue';
import { BackURL } from '../main.js';

export default {
    name: 'LoginView',
    data() {
        return {
            id: sessionStorage.getItem('id'),
            profileList: [],
            userList: [],
            chatList: [],
            otherUser: [{}],
            RoomNumber: '',
            is_set: 3,
        };
    },
    mounted() {
        this.loadProfile();
        this.loadUserList();
        this.loadChatList();
    },
    watch: {
        is_set(newValue) {
            if (newValue === 0) {
                this.loadChatList();
            }
        }
    },
    methods: {
        profileEdit(updatedUser) {
            // 업데이트된 사용자 정보를 처리
            console.log(updatedUser);
            alert('회원 정보를 변경 하시겠습니까?');
            
            axios.post(BackURL+'/updateProfile', updatedUser)
                .then(response => {
                    console.log('Profile updated successfully', response);
                    this.is_set=0;
                    alert('회원 정보가 변경 되었습니다.');
                    this.loadProfile();
                })
                .catch(error => {
                    console.error('Error updating profile:', error);
                });
        },
        join_room(list) {
            console.log(list)
            this.RoomNumber=list.room;
            this.otherUser= [{
                                user_id : list.other_user_name,
                                img : list.other_user_img
                            }]
            this.is_set=1;
            
        },
        join_room_ck(otherUser) {
            if(confirm(otherUser.name+' 님이랑 대화를 하시겠습니까?')){
                const userData = {
                    myid: this.profileList[0].id,
                    myimg: this.profileList[0].img,
                    otherid: otherUser.id,
                    otherimg: otherUser.img,
                };                

                axios.post(BackURL+'/createChat', userData)
                .then(response => {
                    this.RoomNumber = response.data.room;
                    this.otherUser= [{
                                        user_id : otherUser.name,
                                        img : otherUser.img
                                    }]
                    this.is_set=1
                })
                .catch(error => {
                    console.error('Error fetching profile data:', error);
                });
            }
            
        },
        loadProfile() {
            const userData = {
                id: this.id,
            };

            axios.post(BackURL+'/loadProfile', userData)
                .then(response => {
                    if (response.data.length > 0) {
                        this.profileList = response.data;
                    }
                })
                .catch(error => {
                    console.error('Error fetching profile data:', error);
                });
        },
        loadUserList() {
            const userData = {
                id: this.id,
            };

            axios.post(BackURL+'/loadUserList', userData)
                .then(response => {
                    if (response.data.length > 0) {
                        this.userList = response.data;
                    }
                })
                .catch(error => {
                    console.error('Error fetching profile data:', error);
                });
        },
        loadChatList() {
            const userData = {
                id: this.id,
            };

            axios.post(BackURL+'/loadChatList', userData)
            .then(response => {
                if (response.data.length > 0) {
                    this.chatList = response.data;
                    console.log(this.chatList)
                }
            })
            .catch(error => {
                console.error('Error fetching profile data:', error);
            });
        },
    },
    components: {
        MainProfileView,
        MainUserView,
        MainRoomView,
        MainRoomListView,
    }
}
</script>

<style>
.main-contain {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #FCF6F1;
    border-radius: 5px;
    width: 100%;
    height: 100%;
}
.main-header {
    display: flex;
    border-radius: 5px 5px 0 0;
    background: #FCF6F1;
    padding: 15px;
    align-items: center;
}
.main-header h2 {
    margin-left: 20px;
}
.main-footer {
    display: flex;
    justify-content: space-around;
    border-radius: 0 0 5px 5px;
    background: #FCF6F1;
    padding: 20px 0;
    align-items: center;
}
.main-body {
    width: 100%;
    height: 88%;
    background: #cbdced;
    border-radius: 5px 5px 0 0;
}

.icon {
    cursor: pointer;
}
</style>
