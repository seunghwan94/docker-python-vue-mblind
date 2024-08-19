<template>{{totalPosts}}
    <div class="d-flex flex-column">
      <div class="category-buttons">
        <button
          type="button"
          class="btn btn-outline-primary m-2"
          :class="{ active: selectedCategory === key }"
          v-for="(value, key) in categories"
          :key="key"
          @click="selectCategory(key)">
          {{ value }}
        </button>
      </div>
      
      <BoardList 
        :posts="posts"
        :selectedCategory="selectedCategory"
        :totalPosts="totalPosts"
        :currentPage="currentPage"
        :perPage="perPage"
        @updatePage="updatePage"
        @updateStatus="setActiveTab"
      />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import BoardList from './BoardList.vue';
  
  export default {
    data() {
      return {
        selectedCategory: '1',
        categories: {},
        posts: [],
        totalPosts: 0,
        currentPage: 1,
        perPage: 10,
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
          console.log(`${this.$BackURL}/category`);
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
      async fetchPosts(page = this.currentPage) {
        try {
          // Fetch posts
          const postsResponse = await axios.get(`${this.$BackURL}/boardList`, {
            params: {
              category_id: this.selectedCategory,
              page: page,
              per_page: this.perPage
            }
          });
          if (postsResponse.data.status === 'success') {
            this.posts = postsResponse.data.res;
          } else {
            console.error('Failed to fetch posts:', postsResponse.data.message);
          }
  
          // Fetch total posts
          const totalPostsResponse = await axios.get(`${this.$BackURL}/boardListPage`, {
            params: {
              category_id: this.selectedCategory
            }
          });
          console.log(totalPostsResponse.data)
          if (totalPostsResponse.data.status === 'success') {
            this.totalPosts = totalPostsResponse.data.res[0].total_posts;
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
        this.fetchPosts();
      },
      updatePage(page) {
        this.currentPage = page;
        this.fetchPosts(page);
      },
      setActiveTab(tab) {
        // Implement tab switching logic if needed
        console.log('Tab switched to:', tab);
      }
    },
    components: {
      BoardList
    }
  }
  </script>
  
  <style scoped>
  .container {
    padding: 20px;
  }
  .category-buttons {
    margin-bottom: 20px;
  }
  </style>
  