<template>
    <div class="modal" v-if="visible">
      <div class="modal-content">
        <span class="close" @click="$emit('close')">&times;</span>
        <div class="image-grid">
          <img v-for="(img, index) in images" :src="img.src" :key="index" @click="selectImage(img)">
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      images: Array,
      visible: Boolean
    },
    methods: {
      selectImage(img) {
        this.$emit('updateImage', img);
      }
    }
  };
  </script>
  
  <style>
  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0, 0, 0);
    background-color: rgba(0, 0, 0, 0.4);
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  
  .image-grid {
    display: flex;
    flex-wrap: wrap;
  }
  
  .image-grid img {
    margin: 5px;
    width: 100px;
    height: 100px;
    cursor: pointer;
  }
  </style>
  