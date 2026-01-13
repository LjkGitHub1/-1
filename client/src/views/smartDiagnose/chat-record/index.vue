<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useChatRecord } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseChatRecord"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat,
  tableBarButtonsProps
} = useChatRecord(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.chatRecord"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
    :tableBarButtonsProps="tableBarButtonsProps"
  />
</template>
