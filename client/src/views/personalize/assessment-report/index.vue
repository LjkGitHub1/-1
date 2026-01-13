<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useAssessmentReport } from "./utils/hook";
import { ref } from "vue";

// 必须定义组件名，用于菜单匹配
defineOptions({
  name: "AssessmentReport"
});

const tableRef = ref();
// 引入钩子逻辑
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useAssessmentReport(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="assessmentReport"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
