<template>
    <div>
      <div class="d-flex flex-column">
        <div 
          class="card border-primary m-3"
          v-for="post in posts"
          :key="post.board_id"
          @click="postSelect(post.board_id)"
        >
          <div class="card-header d-flex justify-content-between">
            {{ post.category_name }}
            <p class="card-text">{{ post.user_username }}</p>
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ post.title }}</h4>
            <div>{{ stripHtml(post.content) }}</div>
            <div class="d-flex mt-2 justify-content-between">
              <p class="text-body-tertiary pe-2 m-0">{{ formatDate(post.create_date) }}</p>
              <div class="d-flex justify-content-end">
                <p class="text-body-tertiary pe-2 m-0"><i class="bi bi-eye"></i> {{ post.view_count }}</p>
                <p class="text-body-tertiary pe-2 m-0"><i class="bi bi-chat-dots"></i> {{ post.comment_count }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div class="d-flex justify-content-center">
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage <= 1 }">
            <a class="page-link" @click.prevent="changePage(currentPage - 1)" aria-label="Previous">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li 
            class="page-item" 
            v-for="page in totalPages" 
            :key="page" 
            :class="{ active: page === currentPage }"
          >
            <a class="page-link" @click.prevent="changePage(page)">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage >= totalPages }">
            <a class="page-link" @click.prevent="changePage(currentPage + 1)" aria-label="Next">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BoardList',
    props: {
      posts: {
        type: Array,
        default: () => []
      },
      totalPosts: {
        type: Number,
        default: 0
      },
      currentPage: {
        type: Number,
        default: 1
      },
      perPage: {
        type: Number,
        default: 10
      }
    },
    computed: {
      totalPages() {
        return Math.ceil(this.totalPosts / this.perPage);
      }
    },
    methods: {
      postSelect(postId) {
        // Handle post selection
        console.log('Post selected:', postId);
      },
      stripHtml(html) {
        let doc = new DOMParser().parseFromString(html, 'text/html');
        let text = doc.body.textContent || "";
        if (text.length > 20) {
          text = text.substring(0, 20) + "...";
        }
        return text;
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
      changePage(page) {
        if (page >= 1 && page <= this.totalPages) {
          this.$emit('updatePage', page);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .card {
    cursor: pointer;
  }
  </style>
  