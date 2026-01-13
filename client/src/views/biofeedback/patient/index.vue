<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { usePatient } from "./utils/hook";
import { ref } from "vue";

// 组件名称必须定义，用于菜单自动匹配
defineOptions({ name: "BiofeedbackPatient" });

const tableRef = ref();
const {
  api,
  auth,
  listColumnsFormat,
  searchColumnsFormat,
  operationButtonsProps,
  addOrEditOptions
} = usePatient();
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="biofeedback"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operation-buttons-props="operationButtonsProps"
    :add-or-edit-options="addOrEditOptions"
    :show-add="auth.add"
    add-text="新增病人"
  />
</template>
