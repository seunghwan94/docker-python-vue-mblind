<template>
  <div class="editor mt-3">
    <BoardWriteBar v-if="editor" :editor="editor" />
    <div class="d-flex mt-2 mb-3">
      <select v-model="category" class="form-select w-25 me-1" id="Category">
        <option value="" disabled>카테고리</option>
        <option v-for="(value, key) in filteredCategories" :key="key" :value="key">{{ value }}</option>
      </select>
      <input v-model="title" class="form-control" placeholder="제목을 입력하세요">
    </div>
    <div ref="editorElement" class="editor-content"></div>
  </div>
  <div class="d-flex justify-content-end">
    <button type="button" class="btn btn-primary mt-3 mb-3" @click="handleSubmit">
      {{ selectBoard ? '편집' : '게시' }}
    </button>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { Editor } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";
import TextAlign from "@tiptap/extension-text-align";
import Link from "@tiptap/extension-link";
import Image from "@tiptap/extension-image";
import BoardWriteBar from "./BoardWriteBar.vue";

export default {
  components: {
    BoardWriteBar,
  },
  computed: {
    // 전체 카테고리 지우기
    filteredCategories() {
      return Object.entries(this.categories).reduce((acc, [key, value]) => {
        if (key !== '0') {
          acc[key] = value;
        }
        return acc;
      }, {});
    }
  },
  setup(props) {
    const editor = ref(null);
    const editorElement = ref(null);
    const title = ref(props.selectBoard?.title || "");
    const category = ref(props.selectBoard?.category_id || "");
    const user_id = ref(sessionStorage.getItem("user_id"));
    const isEditMode = computed(() => !!props.selectBoard); // 편집 모드인지 확인
    const content = computed(() => props.selectBoard?.content || "<p>여기에 내용을 입력하세요.</p>");

    onMounted(() => {
      editor.value = new Editor({
        element: editorElement.value,
        extensions: [StarterKit, Underline, TextAlign, Link, Image],
        content: content.value,
      });
    });

    onBeforeUnmount(() => {
      if (editor.value) {
        editor.value.destroy();
      }
    });

    const handleSubmit = () => {
      const postContent = editor.value.getHTML();
      if (!title.value || !category.value || !postContent) {
        return alert("모든 필드를 입력해주세요.");
      }

      const payload = {
        title: title.value,
        content: postContent,
        category: category.value,
        user_id: user_id.value,
      };

      const apiURL = isEditMode.value ? `${props.BackURL}/boardPosttingEdit` : `${props.BackURL}/boardPostting`;

      // 편집 시 board_id 포함
      if (isEditMode.value) { payload.board_id = props.selectBoard.board_id; }

      axios.post(apiURL, payload)
        .then((res) => {
          if (res.data.status === "success") {
            alert(isEditMode.value ? "게시글이 수정되었습니다." : "게시글이 작성되었습니다.");
            window.location.reload();
          } else {
            alert("처리 중 오류가 발생했습니다.");
          }
        })
        .catch(() => alert("서버 오류가 발생했습니다."));
    };

    return { editor, editorElement, title, category, handleSubmit };
  },
  props: {
    categories: Object,
    BackURL: String,
    selectBoard: Object,
  },
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
</style>
