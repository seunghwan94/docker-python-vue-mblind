<template>
    <div class="d-flex flex-wrap">
        <PhotoProfile v-for="(userprofile,index) in user_list" :key="index" :userprofile="userprofile"/>
    </div>
    <Pagintion :totalPosts="totalPosts" :currentPage="currentPage" :perPage="perPage" @updatePage="updatePage"/>
</template>
<script>
import axios  from 'axios';
import PhotoProfile from './PhotoProfile.vue';
import Pagintion from '../Pagintion.vue';

export default {
    data(){
        return{
            user_list: [],
            // 페이징
            totalPosts: 0,
            currentPage: 1,
            perPage: 10,
        }
    },
    components:{
        PhotoProfile,
        Pagintion
    },
    mounted() {
        this.userList();
    },
    methods: {
        userList(page = this.currentPage){
            axios.get(`${this.$BackURL}/userList`, {
                params: {
                    page: page,
                    per_page: this.perPage
                }
            }).then(response => {
                console.log(response.data);
                if (response.data.status == 'success') {
                    this.user_list = response.data.res;
                    this.userListTotal();
                } else {
                    console.log('오류발생 새로고침해주세요.');
                }
            }).catch(error => {
                alert('Theme오류 새로고침해주세요.');
                console.error('Error uploading file:', error);
            });
        },
        userListTotal(){
            axios.get(`${this.$BackURL}/userListPage`, {

            }).then(response => {
                if (response.data.res[0].total_photos == 0){
                // 데이터가 없는경우
                this.totalPosts = 1; 
                }else{
                this.totalPosts = response.data.res[0].total_photos;
                }
            }).catch(error => {
                alert('Theme오류 새로고침해주세요.');
                console.error('Error uploading file:', error);
            });
        },
        // async fetchPhoto(page = this.currentPage) {

    
        //     // total posts
        //     const totalPostsResponse = await axios.get(`${this.$BackURL}/boardListPage`, {
        //         params: {
        //         category_id: this.selectedCategory
        //         }
        //     });
        //     // response
        //     if (totalPostsResponse.data.status === 'success') {
        //         if (totalPostsResponse.data.res[0].total_posts == 0){
        //         // 데이터가 없는경우
        //         this.totalPosts = 1; 
        //         }else{
        //         this.totalPosts = totalPostsResponse.data.res[0].total_posts;
        //         }
        //     } else {
        //         console.error('Failed to fetch total posts:', totalPostsResponse.data.message);
        //     }
        //     } catch (error) {
        //     console.error('Error fetching posts or total posts:', error);
        //     }
        // },
    }
}
</script>
<style>

</style>