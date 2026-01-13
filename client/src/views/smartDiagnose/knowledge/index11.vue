<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useKnowledge } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "KnowledgeManage11" // 用于菜单自动匹配组件
});

const tableRef = ref();
const {
  api,
  auth,
  listColumnsFormat,
  searchColumnsFormat,
  tableBarButtonsProps,
  operationButtonsProps
} = useKnowledge(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="knowledge"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :tableBarButtonsProps="tableBarButtonsProps"
    :operationButtonsProps="operationButtonsProps"
    :page-params="{ pageKey: 'page', limitKey: 'limit' }"
  />
</template>
