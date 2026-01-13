<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useArtGeneration } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseArtGeneration"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useArtGeneration(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.artGeneration"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
