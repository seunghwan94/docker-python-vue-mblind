<template>
    <div class="editor mt-3">
      <BoardWriteBar v-if="editor" :editor="editor" />
      <div class="d-flex mt-2 mb-3">
        <select v-model="category" class="form-select w-25 me-1" id="Category">
          <option value="" disabled>카테고리</option>
          <option v-for="(value, key) in categories" :key="key" :value="key">{{ value }}</option>
        </select>
        <input v-model="title" class="form-control" placeholder="제목을 입력하세요">
      </div>
      <div ref="editorElement" class="editor-content"></div>
    </div>
    <div class="d-flex justify-content-end">
      <button type="button" class="btn btn-primary mt-3 mb-3" @click="BoardWrite">Save</button>
    </div>
  </template>
  
  <script>
// npm install @tiptap/vue-3 @tiptap/starter-kit @tiptap/extension-underline @tiptap/extension-text-align @tiptap/extension-link @tiptap/extension-image
  import axios  from 'axios';
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { Editor } from '@tiptap/vue-3';
  import StarterKit from '@tiptap/starter-kit';
  import Underline from '@tiptap/extension-underline';
  import TextAlign from '@tiptap/extension-text-align';
  import Link from '@tiptap/extension-link';
  import Image from '@tiptap/extension-image';
  import BoardWriteBar from './BoardWriteBar.vue';
  export default {
    components: {
      BoardWriteBar,
    },
    setup(props) {
      const editor = ref(null);
      const editorElement = ref(null);
      const title = ref('');
      const category = ref(''); // 새로 추가된 부분
      const user_id = ref(sessionStorage.getItem('user_id'));  // `setup` 함수 내부에서 정의

      onMounted(() => {
        editor.value = new Editor({
          element: editorElement.value,
          extensions: [
            StarterKit,
            Underline,
            TextAlign.configure({
              types: ['heading', 'paragraph'],
            }),
            Link,
            Image,
          ],
          content: '<p>여기에 내용을 입력하세요.</p>',
        });
      });
      onBeforeUnmount(() => {
        if (editor.value) {
          editor.value.destroy();
        }
      });
      const BoardWrite = () => {

        const content = editor.value.getHTML();
        console.log('Category:', category.value); // 새로 추가된 부분
        console.log('Title:', title.value);
        console.log('Content:', content);
        console.log('user_id:', user_id.value);

        if (content && title.value && category.value) {
              // axios.post(`${this.$BackURL}/boardPostting`, {
              axios.post(`${props.BackURL}/boardPostting`, {
                  content: content,
                  title: title.value,
                  category: category.value,
                  user_id: user_id.value
              }).then(res => {
                  console.log(res.data);
                  if (res.data.status === 'success') {
                    alert('게시글이 작성 되었습니다.')
                    window.location.reload();
                  }else{
                    alert('postting 에러');
                  }
              }).catch(e => {
                  console.error('에러', e); 
                  alert('서버 에러');
              });
          } else {
            alert('공백이 있습니다.');
          }
      };
      return { editor, editorElement, title, category, BoardWrite }; // category 추가
    },
    props: {
      categories:Object,
      BackURL: String, 
    }
  };
  </script>
  
  <style scoped>
  .editor {
    border: 1px solid #ddd;
    border-radius: 4px;
    min-height: 50vh;
    padding: 16px;
  }
  .editor-content {
    min-height: 200px;
  }
  hr {
    margin: 20px 0;
    border: none;
    border-top: 1px solid #ddd;
  }
  </style>