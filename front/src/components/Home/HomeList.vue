<template>
  <div class="list-group mt-2 mb-2">
    <a href="/board" class="d-flex list-group-item list-group-item-action active" style="justify-content: space-between;align-items: center;">
      <div>{{ title }}</div>
      <div style=" font-size: 13px;">더보기 > </div>
    </a>
    <div class="card-text d-flex" style="border-left: 1px solid #eceeef;border-right: 1px solid #eceeef;align-items: center;justify-content: space-between; width: 100%;">
      <p class="m-0 ms-4" style="font-weight: bold;">카테고리</p>
      <p class="m-0 ms-3" style="width: 40%;font-weight: bold;">제목</p>
      <div class="d-flex" style="width: 35%;justify-content: space-between;align-items: center;">
        <div class="d-flex" style="align-items: center;">
          <p class="text-body p-2 m-0 ms-3" style="font-weight: bold;">작성자</p>
        </div>
        <p class="text-body-tertiary pe-2 m-0"> </p>
        <p class="text-body pe-2 m-0 me-5" style="font-weight: bold;">게시날짜</p>
      </div>
    </div>
    <a v-for="(value, index) in listValue" :key="index"  href="#" class="list-group-item list-group-item-action">
      <div class="d-flex" style="justify-content: space-between;align-items: center;">
        <p class="m-0 ms-3">{{ value.category_name }}</p>
        <p class="m-0 ms-3" style="width: 40%;">{{ value.title }}</p>

        <div class="d-flex" style="width: 35%;justify-content: space-between;align-items: center;">
          <div class="d-flex" style="align-items: center;">
            <img :src="require(`../../assets/img/${value.img}`)" style="width: 35px;height:35px; border-radius: 50%; cursor: pointer;">
            <p class="text-body p-2 m-0">{{ value.name }}</p>
          </div>
          <p class="text-body-tertiary pe-2 m-0"><i class="bi bi-eye"></i> {{ value.view_cnt }} <i class="bi bi-chat-dots"></i> {{ value.comment_cnt }}</p>
          <p class="text-body-tertiary pe-2 m-0 me-3">{{ formatDate(value.create_date) }}</p>
        </div>
      </div>
    </a>
  </div>
</template>
<script>
export default{
  props:{
    listValue : Object,
    title : String,
  },
  methods:{
    formatDate(dateString) {
        let date = new Date(dateString);
        let year = date.getFullYear();
        let month = ('0' + (date.getMonth() + 1)).slice(-2);
        let day = ('0' + date.getDate()).slice(-2);
        let hours = ('0' + date.getHours()).slice(-2);
        let minutes = ('0' + date.getMinutes()).slice(-2);
        return `${year}-${month}-${day} ${hours}:${minutes}`;
      },
  },
  stripHtml(html) {
    let doc = new DOMParser().parseFromString(html, 'text/html');
    let text = doc.body.textContent || "";
    if (text.length > 20) {
      text = text.substring(0, 20) + "...";
    }
    return text;
  },
}
</script>
<style>

</style>