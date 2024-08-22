<template>
    <div class="card border-success mb-3" style="max-width: 100%">
        <!-- 게시글 헤더 -->
        <div class="card-header d-flex" style="justify-content: space-between;">
            {{ selectBoard.category_name }}
            <p class="card-text">{{ selectBoard.user_username }}</p>
        </div>
        <div class="card-body">
            <div class="d-flex justify-content-between">
                <!-- 게시글 제목 -->
                <h4 class="card-title mt-3 mb-3">{{ selectBoard.title }}</h4>
                <!-- 게시글 dropdown -->
                <div class="dropdown">
                    <div type="button" @click="toggleDropdown" style="cursor: pointer;">
                        <i class="bi bi-three-dots-vertical"></i>
                    </div>
                    <div class="dropdown-menu show" v-if="dropdownVisible" >
                        <button class="dropdown-item" @click="editBoard(selectBoard.board_id)">수정</button>
                        <button class="dropdown-item" @click="deleteBoard(selectBoard.board_id)">삭제</button>
                    </div>
                </div>
            </div>
            <!-- 게시글 내용 -->
            <div v-html="selectBoard.content"></div>
            <!-- 게시글 footer -->
            <div class="d-flex mt-5" style="justify-content: space-between;">
                <p class="text-body-tertiary pe-2 m-0">{{ formatDate(selectBoard.create_date) }}</p>
                <div class="d-flex justify-content-end">
                    <p class="text-body-tertiary pe-2 m-0"><i class="bi bi-eye"></i> {{ selectBoard.view_count + 1 }}</p>
                    <p class="text-body-tertiary pe-2 m-0"><i class="bi bi-chat-dots"></i> {{ commentCount }} </p>
                </div>
            </div>
        </div>
        <!-- 댓글 -->
        <BoardComment :board_id="selectBoard.board_id" @formatDate="formatDate"/>
    </div>
</template>
<script>
import axios from 'axios';
import BoardComment from './BoardComment.vue';

export default {
    data() {
        return {
            commentCount: this.selectBoard.comment_count,
            dropdownVisible: false,
        };
    },
    components:{
        BoardComment,
    },
    props: {
        selectBoard:Object,
    },
    methods:{
        toggleDropdown() {
            this.dropdownVisible = !this.dropdownVisible;
        },
        editBoard(board_id) {
            this.dropdownVisible = false;
            this.$emit('SelectPost',board_id, true)
        },
        // 게시글 삭제
        async deleteBoard(board_id) {
            if(confirm('정말로 삭제하시겠습니까?')){
                try {
                    const response = await axios.post(`${this.$BackURL}/deleteBoard`, {
                        board_id: board_id
                    });
                    if (response.data.status === 'success') {
                        alert('게시글이 삭제 되었습니다.');
                        window.location.href = `${this.$FrontURL}/board`;
                    } else {
                        console.error('Failed to fetch comments:', response.data.message);
                    }
                } catch (error) {
                    console.error('Error fetching comments:', error);
                }
            }
        },
        formatDate(dateString) {
            let date = new Date(dateString);
            let year = date.getFullYear();
            let month = ('0' + (date.getMonth() + 1)).slice(-2);
            let day = ('0' + date.getDate()).slice(-2);
            let hours = ('0' + date.getHours()).slice(-2);
            let minutes = ('0' + date.getMinutes()).slice(-2);
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        },
        

    }
}
</script>
<style>

</style>