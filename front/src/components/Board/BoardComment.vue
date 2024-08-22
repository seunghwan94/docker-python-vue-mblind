<template>
    <div class="card bg-light m-2" style="max-width: 100%;">
        <div class="card-header">댓글</div>
        <div v-if="comments.length > 0" class="d-flex p-3 pb-0 " style="flex-direction: column;">
            <div v-for="(commentdata, index) in comments" :key="index" class="card border-light mb-3" style="max-width: 100%;">
                <div class="card-body align-items-center d-flex" style="flex-direction: row;">
                    <!-- 이미지 -->
                    <img :src="require(`../../assets/img/${commentdata.img}`)" style="width: 50px;border-radius: 50%;">
                    <!-- 댓글 -->
                    <div class="w-100 ps-4">
                        <!-- 이름, 편집, 삭제 -->
                        <div class="d-flex" style="align-items: center; justify-content: space-between;">
                            <p style="font-weight: bold; margin:0;">{{ commentdata.name }}</p>
                            <div class="d-flex" v-if="commentdata.name === user_name">
                                <div type="button" class="m-0" style="font-size: 16px;" @click="commentEdit(index)"><i class="bi bi-pencil-square"></i></div>
                                <div type="button" class="m-0 ms-1" style="font-size: 16px;" @click="commentDelete(index, commentdata.id)"><i class="bi bi-trash"></i></div>
                            </div>
                        </div>
                        <!-- 댓글 편집 -->
                        <div v-if="commentdata.isEditing">
                            <textarea class="form-control" v-model="commentdata.editContent" rows="2"></textarea>
                            <div class="d-flex mt-2 mb-2" style="justify-content: flex-end;">
                                <button class="btn btn-primary btn-sm " @click="saveCommentEdit(index, commentdata.id)">수정</button>
                                <button class="btn btn-secondary btn-sm  ms-2" @click="cancelEdit(index)">취소</button>
                            </div>
                        </div>
                        <!-- 댓글 view -->
                        <p v-else class="card-text m-0">{{ commentdata.content }}</p>
                        <p class="text-body-tertiary m-0" style="text-align: end; font-size: 13px;">{{ sendformatDate(commentdata.create_date) }}</p>
                    </div>
                </div>
            </div>
            <hr style="margin-bottom:0"/>
        </div>
        <div class="card-body d-flex pb-0">
            <div class="d-flex" style="align-items: flex-start">
                <img :src="require(`../../assets/img/${user_img}`)" style="width: 50px;border-radius: 50%;">
            </div>
            <div class="form-control ms-2" id="comment" style="height: auto; min-height: 80px;">
                <div contenteditable="false" style="font-weight: bold;">{{ user_name }}</div>
                <div contenteditable="true" ref="editableContent" @input="updateComment" style="outline: none; border: 2px solid transparent;"></div>
            </div>
        </div>
        <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-outline-primary m-3" @click="commentAdd(board_id)">등록</button> 
        </div>
    </div>

</template>
<script>
import axios from 'axios';

export default {
    data(){
        return{
            user_img: sessionStorage.getItem('user_img'),
            user_name: sessionStorage.getItem('user_name'),
            comments:[],
            editContent: '',
            commentText: '',
        }
    },
    props:{
        board_id: String,
    },
    mounted() {
        this.commentList();
    },
    methods: {
        // 댓글 목록 가져오기
        async commentList() {
            try {
                const response = await axios.get(`${this.$BackURL}/commentList`, {
                    params: {
                        board_id: this.board_id
                    }
                });
                if (response.data.status === 'success') {
                    this.comments = response.data.res.map(comment => ({
                        ...comment,
                        isEditing: false,
                        editContent: ''
                    }));
                } else {
                    console.error('Failed to fetch comments:', response.data.message);
                }
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        },
        // 댓글 편집
        commentEdit(index) {
            this.comments[index].isEditing = !this.comments[index].isEditing;
            if (this.comments[index].isEditing) {
                this.comments[index].editContent = this.comments[index].content;
            }
        },
        // 편집 취소
        cancelEdit(index) {
            this.comments[index].isEditing = false;
        },
        // 댓글 수정
        async saveCommentEdit(index, comment_id) {
            if (confirm("수정하시겠습니까?")) {
                const editedComment = this.comments[index].editContent;
                try {
                    const response = await axios.post(`${this.$BackURL}/saveCommentEdit`, {
                        comment_id: comment_id,
                        content: editedComment
                    });
                    if (response.data.status === 'success') {
                        this.comments[index].content = editedComment;
                        this.comments[index].isEditing = false;
                    } else {
                        console.error('Failed to edit comment');
                    }
                } catch (error) {
                    console.error('Error editing comment:', error);
                }
            }
        },
        // 댓글 삭제
        async commentDelete(index, comment_id) {
            if (confirm("삭제하시겠습니까?")) {
                try {
                    const response = await axios.post(`${this.$BackURL}/commentDelete`, {
                        comment_id: comment_id
                    });
                    if (response.data.status === 'success') {
                        this.comments.splice(index, 1); // 배열에서 해당 댓글을 완전히 제거합니다.
                        this.commentCount -= 1;         // 댓글 수를 하나 줄입니다.
                    } else {
                        console.error('Failed to delete comment');
                    }
                } catch (error) {
                    console.error('Error deleting comment:', error);
                }
            }
        },
        async commentAdd(board_id) {
            try {
                const user_id = sessionStorage.getItem('user_id');
                const comment = this.commentText;
                const response = await axios.get(`${this.$BackURL}/commentAdd`, {
                    params: {
                        board_id: board_id,
                        user_id: user_id,
                        comment: comment
                    }
                });
                if (response.data.status === 'success') {
                    this.commentList();
                    this.commentText = '';
                    this.$refs.editableContent.innerText = '';
                    this.commentCount = this.commentCount + 1;
                    alert('댓글이 등록되었습니다.');
                } else {
                    console.log('댓글 등록 실패');
                }
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        },
        // 날짜 선정
        sendformatDate(create_date){
            this.$emit('formatDate', create_date);
        },
        updateComment(event) {
            this.commentText = event.target.innerText;
        },
    }
}
</script>
<style>
div[contenteditable="true"]:focus {
    border-color: #5FC8A5;
}
</style>