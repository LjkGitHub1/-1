<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useModelConfig } from "./utils/hook";
import { ref } from "vue";

// 按文档规范：必须定义组件名，用于菜单自动匹配
defineOptions({
  name: "SmartDiagnoseModelConfig"
});

const tableRef = ref();
// 引入钩子逻辑
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useModelConfig(tableRef);
</script>

<template>
  <!-- 按文档规范：使用RePlusPage组件，传递所有钩子返回参数 -->
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.modelConfig"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
