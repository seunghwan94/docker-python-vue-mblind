<template>
    <div class="main-user-contain" @click="$emit('join_room',list)">
        <img :src="list? require(`../assets/img/${list.other_user_img}`): ''" style="width: 10%; border-radius: 50%;">
        <div class="room-contants">
            <p class="room-title"> {{ list? list.other_user_name : '' }} </p>
        </div>
    </div>
</template>

<script>

export default {
    props:{
        list: Object,
    }
}

</script>
<style>
.main-user-contain {
    display: flex;
    background: #cbdced;
    padding: 15px;
    align-items: center;
    border-bottom: 1px solid gray;
    cursor: pointer;
}
.room-contants {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.room-contants .room-title{
    margin: 0 0 0 20px;
    font-weight: bold;
    font-size: 17px;
}
.room-contants .room-subtitle{
    margin: 5px 0 0 25px;
    color: gray;
    font-size: 14px;
}
</style>