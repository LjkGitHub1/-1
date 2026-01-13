<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useEmotionRecognition } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseEmotionRecognition"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useEmotionRecognition(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.emotionRecognition"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
