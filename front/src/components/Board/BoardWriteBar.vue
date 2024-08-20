<template>
    <div v-if="editor" class="menu-bar">
      <button @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
        B
      </button>
      <button @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
        I
      </button>
      <button @click="editor.chain().focus().toggleUnderline().run()" :class="{ 'is-active': editor.isActive('underline') }">
        U
      </button>
      <button @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
        S
      </button>
      <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
        H1
      </button>
      <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
        H2
      </button>
      <button @click="editor.chain().focus().setTextAlign('left').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }">
        ←
      </button>
      <button @click="editor.chain().focus().setTextAlign('center').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }">
        ↔
      </button>
      <button @click="editor.chain().focus().setTextAlign('right').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }">
        →
      </button>
      <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
        •
      </button>
      <button @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
        1.
      </button>
      <button @click="setLink">
        🔗
      </button>
      <label for="image-upload" class="image-upload-label">
        📷
        <input
          type="file"
          id="image-upload"
          @change="uploadImage"
          accept="image/*"
          style="display: none;"
        />
      </label>
    </div>
  </template>

  <script>
  export default {
    props: {
      editor: {
        type: Object,
        required: true,
      },
    },
    methods: {
      setLink() {
        const url = window.prompt('URL:')
        if (url) {
          this.editor.chain().focus().setLink({ href: url }).run()
        } else {
          this.editor.chain().focus().unsetLink().run()
        }
      },
      async uploadImage(event) {
        const file = event.target.files[0];
        if (!file) return;
  
        const formData = new FormData();
        formData.append('image', file);
  
        try {
          const response = await fetch('/api/upload-image', {
            method: 'POST',
            body: formData,
          });
  
          if (!response.ok) throw new Error('Image upload failed');
  
          const data = await response.json();
          
          this.editor.chain().focus().setImage({ src: data.imageUrl }).run();
        } catch (error) {
          console.error('Error uploading image:', error);
          alert('Failed to upload image. Please try again.');
        }
      },
    },
  };
  </script>

  <style scoped>
  .menu-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px;
    border-bottom: 1px solid #ddd;
  }
  
  button, .image-upload-label {
    background: none;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    padding: 4px 8px;
    font-size: 14px;
  }
  
  button.is-active {
    background-color: #e9ecef;
    font-weight: bold;
  }
  
  .image-upload-label:hover {
    background-color: #f0f0f0;
  }
  </style>