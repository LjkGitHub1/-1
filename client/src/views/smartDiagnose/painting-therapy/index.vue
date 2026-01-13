<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { usePaintingTherapy } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnosePaintingTherapy"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = usePaintingTherapy(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.paintingTherapy"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
