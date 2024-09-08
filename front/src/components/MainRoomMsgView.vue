<template>
    <div class="msg-list">
        <div v-for="(msg, i) in msgList" :key="i" :class="{'my-msg-contain': msg.sender === 'me', 'you-msg-contain': msg.sender === 'you', 'bot-msg-contain': msg.sender === 'bot'}">
            <div v-if="msg.sender === 'you'">
                <div :style="msg.sender === 'bot'? 'display:none':' ' "><img :src="require(`@/assets/img/${msg.img}`)" style="width: 50px; height: auto;"></div>
            </div>
            <div>
                <div v-if="msg.sender === 'you'">
                    <div style="font-size: 13px;text-align: left; padding-left: 8px;" :style="msg.sender === 'bot'? 'display:none':' ' ">{{ msg.id }}</div>
                </div>
                <div v-else>
                    <div style="font-size: 13px;text-align: right; padding-right: 8px;" :style="msg.sender === 'bot'? 'display:none':' ' ">{{ id }}</div>
                </div>
                <div :class="msg.sender === 'me' ? 'my-msg' : msg.sender === 'you' ? 'you-msg' : 'bot-msg'">{{ msg.text }}</div>
            </div>
            <div v-if="msg.sender === 'me'">
                <div :style="msg.sender === 'bot'? 'display:none':' ' "><img :src="require(`@/assets/img/${msg.img}`)" style="width: 50px; height: auto;"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props:{
        id:String,
        msgList:Array,
    }
}
</script>

<style>

</style>