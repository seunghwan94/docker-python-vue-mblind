<template>
    <div>
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
    name: 'PaginationBar',
    props: {
      totalPosts: {
        type: Number,
        default: 1
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
      changePage(page) {
        if (page >= 1 && page <= this.totalPages) {
          this.$emit('updatePage', page);
        }
      }
    }
  }
  </script>
  
  <style scoped>
 .pagination {
    cursor: pointer;
 }
  </style>
  