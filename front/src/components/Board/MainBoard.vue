<template>
    <div class="d-flex flex-column">
      <div class="category-buttons" style="margin:10px">
        <button
          type="button"
          class="btn btn-outline-primary m-2"
          :class="{ active: selectedCategory === key }"
          v-for="(value, key) in categories"
          :key="key"
          @click="selectCategory(key)"
          >
          {{ value }}
        </button>
      </div>
      <!-- 게시판 목록 -->
      <div v-if="status == 'BoardList'"> 
        <BoardList :posts="posts" :selectedCategory="selectedCategory" @SelectPost="SelectPost"/>
        <div class="d-flex justify-content-end">
          <button type="button" class="btn btn-outline-primary m-2" @click="startWriting">글쓰기</button>
        </div>
        <Pagintion :totalPosts="totalPosts" :currentPage="currentPage" :perPage="perPage" @updatePage="updatePage"/>
      </div>
      <!-- 게시판 보기 -->
      <BoardView v-else-if="status == 'BoardView'" :selectBoard="selectBoard" @SelectPost="SelectPost"/> 
      <!-- 글쓰기 -->
      <BoardWrite v-else-if="status == 'BoardWrite'" :categories="categories" :BackURL="BackURL" :selectBoard="selectBoard"/>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import BoardList from './BoardList.vue';
  import BoardView from './BoardView.vue';
  import BoardWrite from './BoardWrite.vue';
  import Pagintion from '../Pagintion.vue';
  
  export default {
    data() {
      return {
        user_id: sessionStorage.getItem('user_id'),
        posts: [],              // 게시글
        status: 'BoardList',    // 상태관리
        BackURL: this.$BackURL, // 글쓰기할때 setup 사용( this 작동 안함 )
        selectBoard: '',        // 게시글 선택
        // 페이징
        totalPosts: 0,
        currentPage: 1,
        perPage: 10,
        // 카테고리 목록 및 선택
        categories: {},
        selectedCategory: '1',  
      }
    },
    created() {
      this.fetchCategories();
      this.fetchPosts();
    },
    watch: {
        // Watcher for selectedCategory
        selectedCategory(newCategory, oldCategory) {
            if (newCategory !== oldCategory) {
                this.currentPage = 1; // Reset to the first page when category changes
                this.posts = [],
                this.fetchPosts(); // Fetch posts for the new category
            }
        }
    },
    methods: {
      async fetchCategories() {
        try {
          const response = await axios.get(`${this.$BackURL}/category`);
          if (response.data.status === 'success') {
            this.categories = response.data.res.reduce((acc, category) => {
              acc[category.id] = category.name;
              return acc;
            }, {});
          } else {
            console.error('Failed to fetch categories:', response.data.message);
          }
        } catch (error) {
          console.error('Error fetching categories:', error);
        }
      },
      async BoardViewCount(board_id) {
        try {
          const response = await axios.get(`${this.$BackURL}/boardViewCnt`, {
            params: {
              user_id: this.user_id,
              board_id: board_id
            }
          });
          console.log('Response status:', response.data.status);
        } catch (error) {
          console.error('Error fetching board view count:', error);
        }
      },
      async fetchPosts(page = this.currentPage) {
        try {
          // api 요청 
          const postsResponse = await axios.get(`${this.$BackURL}/boardList`, {
            params: {
              category_id: this.selectedCategory,
              page: page,
              per_page: this.perPage
            }
          });
          // response
          if (postsResponse.data.status === 'success') {
            this.posts = postsResponse.data.res;
          } else {
            console.error('Failed to fetch posts:', postsResponse.data.message);
          }
  
          // total posts
          const totalPostsResponse = await axios.get(`${this.$BackURL}/boardListPage`, {
            params: {
              category_id: this.selectedCategory
            }
          });
          // response
          if (totalPostsResponse.data.status === 'success') {
            if (totalPostsResponse.data.res[0].total_posts == 0){
              // 데이터가 없는경우
              this.totalPosts = 1; 
            }else{
              this.totalPosts = totalPostsResponse.data.res[0].total_posts;
            }
          } else {
            console.error('Failed to fetch total posts:', totalPostsResponse.data.message);
          }
        } catch (error) {
          console.error('Error fetching posts or total posts:', error);
        }
      },
      selectCategory(key) {
        this.selectedCategory = key;
        this.currentPage = 1; // Reset to the first page when category changes
        this.status = 'BoardList';
        this.fetchPosts();
      },
      updatePage(page) {
        this.currentPage = page;
        this.fetchPosts(page);
      },
      startWriting() {
        this.selectBoard = ''; // selectBoard를 공백으로 초기화
        this.changeStatus('BoardWrite'); // 상태 변경
      },
      SelectPost(board_id,edit=false){
        const SelectBoardPost = this.posts.find(board => board.board_id === board_id);
        this.selectBoard = SelectBoardPost;

        if (edit){
          this.changeStatus('BoardWrite');
        }else{
          this.BoardViewCount(board_id);
          this.changeStatus('BoardView');
        }
      },
      changeStatus(target){
        this.status = target;
      },
    },
    components: {
      BoardList,
      BoardView,
      BoardWrite,
      Pagintion,
    }
  }
  </script>
  
  <style>
  .container {
    padding: 20px;
  }
  .category-buttons {
    margin-bottom: 20px;
  }
  /* 기본 카드 스타일 */
  .card.border-primary {
    transition: background-color 0.3s, box-shadow 0.3s, color 0.3s; /* 배경색, 그림자, 글자색에 대해 transition 설정 */
  }
  /* 카드에 마우스 오버 시 효과 */
  .card.border-primary:hover {
    background-color: #78C2AD; /* 배경색 변경 */
    color: white; /* 텍스트 색상 변경 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 카드에 그림자 추가 */
  }
  </style>
  