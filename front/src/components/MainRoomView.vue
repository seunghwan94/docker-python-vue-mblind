<template>
  <div v-if="RoomNumber" class="main-room-contain-y">
      <MainRoomMsgView :id="name" :msgList="msgList"/>

      <div class="text-contain">
          <textarea class="textarea-input" v-model="messageText" @keydown.enter.prevent="onEnter"></textarea>
          <button type="button" class="send-button" @click="sendMsg"><font-awesome-icon class="icon" :icon="['fas', 'arrow-up']" size="2xl"/></button>
      </div>
  </div>
  <div v-else class="main-room-contain-n">
      <div style="display: flex;flex-direction: column;">
          <h3>대화방이 없습니다.</h3>
          <h3>대화방을 선택해주세요.</h3>
      </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
import MainRoomMsgView from './MainRoomMsgView.vue';
import { BackURL } from '../main.js';
import axios from 'axios';

export default {
  props: {
      RoomNumber: String,
      profileList: Array,
      otherUser: Array,
  },
  data(){
      return {
          msgList: [],
          socket: null,
          id: this.profileList[0].user_id,
          img: this.profileList[0].img,
          name: this.profileList[0].name,
          othername: this.otherUser[0].user_id,
          otherimg: this.otherUser[0].img,
          room: this.RoomNumber,
          messageText: ''
      }
  },
  methods: {
      sendMsg() {
          if (this.messageText.trim()) {
              const text = this.messageText;
              const sender = 'me';
              this.msgList.push({ text, sender, id: this.name, img: this.img });

              this.msgListAdd({ 
                room:this.room, 
                text, 
                sender, 
                id: this.name,
                otherid: this.othername, 
                img:this.img,
              });

              this.$nextTick(() => {
                  this.scrollToBottom(); 
              });

              this.socket.emit('user', this.room, text, this.name, this.img);
              this.messageText = '';
          }
      },
      onEnter() {
          this.sendMsg();
      },
      scrollToBottom() {
          const container = this.$el.querySelector('.msg-list');
          if (container) {
              container.scrollTop = container.scrollHeight;
          }
      },

      msgListAdd(insertMsg) {
        axios.post(BackURL+'/msgListAdd', insertMsg)
        .then(response => {
            console.log('msgListAdd insert successfully', response);
        })
        .catch(error => {
            console.error('Error insert profile:', error);
        });
      },

      loadMsgList() {
        const selectData = {
          user_name: this.name,
          room : this.room
        }

        axios.post(BackURL+'/loadMsgList', selectData)
        .then(response => {
          if (Array.isArray(response.data)) {
                response.data.forEach(item => {
                    let sender;
                    let text = item.msg;
                    let id;

                    if (item.user_type === 'bot') {
                        sender = 'bot';
                    } else if (item.user_type === 'you') {
                        sender = 'you';
                        id = item.other_name;
                    } else if (item.user_type === 'me') {
                        sender = 'me';
                        id = item.user_name;
                    }

                    this.msgList.push({ sender, text, img: item.img, id });
                });
            } else {
                console.error('Response data is not an array:', response.data);
            }
        })
        .catch(error => {
            console.error('Error select profile:', error);
        });
      },
  },
  mounted() {
      this.loadMsgList()
      this.socket = io(BackURL);

      this.socket.on('chat message', (msg) => {
          if (msg.senderName !== this.name) {
              this.msgList.push({ text: msg.msg, sender: 'you', id: msg.senderName, img: msg.img });

              this.msgListAdd({ 
                room:this.room, 
                text: msg.msg, 
                sender: 'you', 
                id:this.name,
                img: msg.img,
                otherid:msg.senderName
              });
              this.$nextTick(() => {
                  this.scrollToBottom(); 
              });
          }
      });

      this.socket.on('bot', (msg) => {
          this.msgList.push({ text: msg.msg, sender: 'bot' });
          this.msgListAdd({ 
            room:this.room, 
            text: msg.msg, 
            sender: 'bot', 
            id: this.name,
            img: this.otherimg,
            otherid: this.othername
          });
      });

      this.socket.emit('join room', this.room, this.name);
  },
  components: {
      MainRoomMsgView,
  }
}
</script>

<style>
.main-room-contain-y {
  display: flex;
  background: #cbdced;
  padding: 15px;
  justify-content: center;
  height: 100%;
  flex-direction: column;
}
.main-room-contain-n {
  display: flex;
  background: #cbdced;
  padding: 15px;
  align-items: center;
  justify-content: center;
  height: 100%;
  border-radius: 5px;
}
.msg-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 5px;
  border-radius: 5px;
  background: rgb(246, 245, 245);
  scroll-behavior: smooth;
}
.my-msg-contain {
  display: flex;
  justify-content: flex-end;
}
.you-msg-contain {
  display: flex;
  justify-content: flex-start;
}
.you-msg {
  background: rgb(211, 211, 211);
  border-radius: 10px;
  padding: 7px;
  margin: 5px;
}
.my-msg {
  background: rgb(255, 249, 171);
  border-radius: 10px;
  padding: 7px;
  margin: 5px;
}
.bot-msg {
  margin: 10px;
}
.text-contain {
  display: flex;
  align-items: center;
  margin: 5px 0;
  width: 100%;
  justify-content: flex-end;
  color: #fff;
}
.textarea-input {
  resize: none;
  width: 100%;
  padding: 3px;
  border-radius: 5px 0 0 5px;
  
  border: 1px solid transparent;
}
.send-button {
  width: 15%;
  padding: 5px;
  border-radius: 0 5px 5px 0;
  border: 1px solid transparent;
  cursor: pointer;
  background: #a7c4e0;
  color: #fff;
  font-weight: bold;
}
</style>
