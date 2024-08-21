<template>
    <div>
      <div class="d-flex flex-column" v-if="posts.length > 0">
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
      <div v-else>
        <div class="card border-primary m-3">
          <div class="card-body p-0">
            <div class="card-header d-flex justify-content-between" style="height: 32px;"></div>
            <h5 class="card-title p-4" style="text-align:center;">게시글이 없습니다.</h5>
          </div>
        </div>
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
    }
  }
  </script>
  
  <style>
  .card {
    cursor: pointer;
  }
  </style>
  