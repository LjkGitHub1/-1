<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useEmotionFusion } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseEmotionFusion"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useEmotionFusion(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.emotionFusion"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
