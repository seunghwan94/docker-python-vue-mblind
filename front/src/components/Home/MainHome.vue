<template>
    <div class="card border-light m-3" style=" height: 400px;">
      <div class="image-div"></div>
    </div>
    <!-- <div class="d-flex" style="justify-content: space-between;">
      <HomeNotice /><HomeNotice />
    </div> -->
    <HomeNotice />
    <HomeList v-for="(value, key) in totalList" :key="key" :listValue="value" :title = "key"/>

</template>
<script>
import axios from 'axios';
import HomeList from './HomeList.vue';
import HomeNotice from './HomeNotice.vue';

export default{
  data(){
    return{
      todayBestList : {},
      BestList:{},
      totalList : {},
    }
  },
  components: {
    HomeList,
    HomeNotice,
  },
  async created() {
    await this.Best();
    await this.todayBest();
    this.total();
  },
  methods: {
    async Best() {
      try {
        const response = await axios.post(`${this.$BackURL}/Best`);
        if (response.data.status === 'success') {
          this.BestList = response.data.res;
        } else {
          console.error('Failed to fetch categories:', response.data.message);
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async todayBest() {
      try {
        const response = await axios.post(`${this.$BackURL}/todayBest`);
        if (response.data.status === 'success') {
          this.todayBestList = response.data.res;
        } else {
          console.error('Failed to fetch categories:', response.data.message);
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async total(){
      this.totalList['Best'] = this.BestList;
      this.totalList['todayBest'] = this.todayBestList;
    }
  }
}

</script>
<style>
.image-div {
  width: 100%;
  height: 100%;
  border-radius: 5px;
  background-image: url('../../assets/img/Logo2.png'); /* 이미지 경로 설정 */
  background-size: cover; /* 이미지가 div를 꽉 채우도록 설정 */
  background-position: center; /* 이미지의 중앙을 기준으로 배치 */
  background-repeat: no-repeat; /* 이미지 반복 방지 */
}
</style>