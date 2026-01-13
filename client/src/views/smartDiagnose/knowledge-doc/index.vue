<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useKnowledgeDoc } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseKnowledgeDoc"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useKnowledgeDoc(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.knowledgeDoc"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
