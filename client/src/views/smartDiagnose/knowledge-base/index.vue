<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useKnowledgeBase } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseKnowledgeBase"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useKnowledgeBase(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.knowledgeBase"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
