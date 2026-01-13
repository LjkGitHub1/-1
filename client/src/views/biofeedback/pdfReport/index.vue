<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { usePdfReport } from "./utils/hook";
import { ref } from "vue";

defineOptions({ name: "BiofeedbackPdfReport" });
const tableRef = ref();
const {
  api,
  auth,
  listColumnsFormat,
  searchColumnsFormat,
  operationButtonsProps,
  addOrEditOptions
} = usePdfReport();
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
    add-text="新增PDF报告"
  />
</template>
